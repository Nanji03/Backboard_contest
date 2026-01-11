"""Routes for chat with AI assistant."""

from flask import Blueprint, request, jsonify
from ..models import ChatMessage, ChatResponse
from ..services import safety_service
from ..backboard_client import run_coroutine, ensure_thread, send_message
from ..config import config
import os

chat_bp = Blueprint("chat", __name__, url_prefix="/api")

# Store threads per user (in production, move to database)
user_threads = {}

# System prompts for each role
SENIOR_SYSTEM_PROMPT = """You are a compassionate health companion for an elderly patient. 
Your role is to help explain medications, appointments, and health information in simple, clear language.

CRITICAL RULES:
- Always be warm and supportive in tone.
- Never provide medical advice or suggest changing medications.
- If asked about medication changes, respond: "That's great! Please share this with your doctor at your next visit."
- Use short sentences and avoid medical jargon.
- If you're uncertain, say: "I'm not sure. Please ask your caregiver or doctor."
- Never invent information about the patient's medications or appointments.
- Repeat key details (drug names, times, doses) clearly.
- Flag any conflicting information instead of guessing.

Remember: You're here to support and clarify, not to diagnose or prescribe."""

CAREGIVER_SYSTEM_PROMPT = """You are a clinical decision-support assistant for caregivers and physicians managing elder patient care.
Your role is to help organize medication schedules, explain medical reports, and flag potential concerns.

RULES:
- Provide clear, structured explanations with sources when possible.
- If medication interactions or contraindications are present, flag them clearly.
- Never prescribe or change medications; only caregivers/physicians can do that.
- When a patient requests a medication change, suggest documenting it and discussing with the physician.
- Organize information by date, patient, and action items.
- Be concise but thorough; caregivers need actionable summaries."""

@chat_bp.post("/chat")
def chat():
    """Chat endpoint for seniors and caregivers with role-based safety."""
    data = request.get_json() or {}
    user_id = data.get("userId")
    message = data.get("message", "")
    role = data.get("role", "senior")  # "senior" or "caregiver"
    
    # Validation
    if not user_id or not message:
        return jsonify({"error": "userId and message are required"}), 400
    
    if role not in ["senior", "caregiver"]:
        return jsonify({"error": "role must be 'senior' or 'caregiver'"}), 400
    
    try:
        assistant_id = config.BACKBOARD_ASSISTANT_ID
        if not assistant_id:
            return jsonify({"error": "Assistant not configured"}), 500
        
        # Get or create thread for this user
        if user_id not in user_threads:
            thread = run_coroutine(ensure_thread(assistant_id))
            user_threads[user_id] = thread.thread_id
        
        thread_id = user_threads[user_id]
        
        # Choose system prompt based on role
        system_prompt = SENIOR_SYSTEM_PROMPT if role == "senior" else CAREGIVER_SYSTEM_PROMPT
        
        # Construct full message with system context
        full_message = f"[SYSTEM ROLE: {role.upper()}]\n{system_prompt}\n\n[USER MESSAGE]: {message}"
        
        # Send to Backboard
        reply = run_coroutine(send_message(thread_id, full_message))
        
        # Apply safety checks if senior
        if role == "senior":
            is_safe, safety_note = safety_service.validate_response(reply, message)
            if not is_safe:
                reply = f"{reply}\n\n⚠️ {safety_note}"
        
        # Return structured response
        response = ChatResponse(
            message=reply,
            threadId=thread_id,
            role=role,
            userId=user_id,
            safe=True if role == "caregiver" else is_safe
        )
        
        return jsonify(response.model_dump()), 200
    
    except Exception as e:
        return jsonify({"error": f"Chat failed: {str(e)}"}), 500


@chat_bp.delete("/chat/<user_id>/thread")
def clear_thread(user_id):
    """Clear conversation history for a user (admin only in production)."""
    if user_id in user_threads:
        del user_threads[user_id]
        return jsonify({"message": f"Thread cleared for user {user_id}"}), 200
    return jsonify({"error": "User not found"}), 404

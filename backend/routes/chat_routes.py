"""Routes for chat with AI assistant."""

from flask import Blueprint, request, jsonify
from ..models import ChatMessage, ChatResponse
from ..services import safety_service
from ..backboard_client import run_coroutine, ensure_thread, send_message
import os

chat_bp = Blueprint("chat", __name__, url_prefix="/api")

# Store threads per user
user_threads = {}

@chat_bp.post("/chat")
def chat():
    """Chat endpoint for seniors and caregivers."""
    data = request.get_json() or {}
    user_id = data.get("userId")
    message = data.get("message", "")
    role = data.get("role", "senior")
    
    if not user_id or not message:
        return jsonify({"error": "userId and message are required"}), 400
    
    try:
        assistant_id = os.getenv("BACKBOARD_ASSISTANT_ID")
        if not assistant_id:
            return jsonify({"error": "Assistant not configured"}), 500
        
        # Get or create thread for this user
        if user_id not in user_threads:
            thread = run_coroutine(ensure_thread(assistant_id))
            user_threads[user_id] = thread["thread_id"]
        thread_id = user_threads[user_id]

        # Send message to Backboard
        response = run_coroutine(send_message(thread_id, message, assistant_id))
        ai_reply = response.get("content", "I'm sorry, I couldn't process that.")
        thread_id = response.get("thread_id", thread_id)
        memory_context = response.get("memory_context", {})
        # Update thread mapping
        user_threads[user_id] = thread_id
        chat_response = ChatResponse(
            reply=ai_reply,
            thread_id=thread_id,
            memory_context=memory_context
        ) 
        return jsonify(chat_response.dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

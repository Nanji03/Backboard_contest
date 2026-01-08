"""Routes for appointment management."""

from flask import Blueprint, request, jsonify
from ..models import Appointment
from ..services import appointment_service, safety_service
from ..backboard_client import run_coroutine

appt_bp = Blueprint("appointments", __name__, url_prefix="/api/appointments")

@appt_bp.post("/")
def add_appointment():
    """Add a new appointment for a senior."""
    data = request.get_json()
    senior_id = data.get("senior_id")
    
    if not senior_id:
        return jsonify({"error": "senior_id is required"}), 400
    
    try:
        appt = Appointment(
            date=data.get("date"),
            time=data.get("time"),
            doctor_name=data.get("doctor_name"),
            specialization=data.get("specialization"),
            location=data.get("location"),
            notes=data.get("notes")
        )
        
        result = run_coroutine(appointment_service.save_appointment(senior_id, appt))
        return jsonify({"success": True, "appointment": result}), 201
    
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appt_bp.get("/<senior_id>")
def get_appointments(senior_id):
    """Get all appointments for a senior."""
    try:
        appts = appointment_service.get_appointments(senior_id)
        return jsonify({"appointments": appts}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appt_bp.get("/<senior_id>/next")
def get_next_appointment(senior_id):
    """Get the next upcoming appointment."""
    try:
        appt = appointment_service.get_next_appointment(senior_id)
        return jsonify({"next_appointment": appt}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@appt_bp.put("/<senior_id>/<appt_id>")
def update_appointment(senior_id, appt_id):
    """Update appointment status."""
    data = request.get_json()
    status = data.get("status")
    
    if not status:
        return jsonify({"error": "status is required"}), 400
    
    try:
        success = appointment_service.update_appointment(senior_id, appt_id, status)
        if success:
            return jsonify({"success": True, "message": "Appointment updated"}), 200
        else:
            return jsonify({"error": "Appointment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

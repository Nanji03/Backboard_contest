"""Medication management routes."""

from flask import Blueprint, request, jsonify
from ..models import Medication, MedicationList, MedicationUpdate
from ..services import medication_service

med_bp = Blueprint("medications", __name__, url_prefix="/api/medications")

@med_bp.get("/<user_id>")
def get_medications(user_id):
    """Get all medications for a user."""
    try:
        meds = medication_service.get_user_medications(user_id)
        return jsonify({"userId": user_id, "medications": meds}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@med_bp.post("/<user_id>")
def add_medication(user_id):
    """Add a new medication for a user (caregiver only)."""
    data = request.get_json() or {}
    
    try:
        med = Medication(
            name=data.get("name"),
            dose=data.get("dose"),
            frequency=data.get("frequency"),
            instructions=data.get("instructions", "")
        )
        
        result = medication_service.add_medication(user_id, med)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@med_bp.put("/<user_id>/<med_id>")
def update_medication(user_id, med_id):
    """Update a medication (caregiver only)."""
    data = request.get_json() or {}
    
    try:
        update = MedicationUpdate(medicationId=med_id, **data)
        result = medication_service.update_medication(user_id, update)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@med_bp.delete("/<user_id>/<med_id>")
def delete_medication(user_id, med_id):
    """Delete a medication (caregiver only)."""
    try:
        medication_service.delete_medication(user_id, med_id)
        return jsonify({"message": "Medication deleted"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

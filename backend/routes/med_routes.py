"""Routes for medication management."""

from flask import Blueprint, request, jsonify
from ..models import Medication
from ..services import medication_service, safety_service
from ..backboard_client import run_coroutine

med_bp = Blueprint("medications", __name__, url_prefix="/api/medications")

@med_bp.post("/")
def add_medication():
    """Add a new medication for a senior."""
    data = request.get_json()
    senior_id = data.get("senior_id")
    
    if not senior_id:
        return jsonify({"error": "senior_id is required"}), 400
    
    try:
        med = Medication(
            name=data.get("name"),
            dosage=data.get("dosage"),
            dose_quantity=int(data.get("dose_quantity", 1)),
            frequency=data.get("frequency"),
            instructions=data.get("instructions")
        )
        
        result = run_coroutine(medication_service.save_medication(senior_id, med))
        return jsonify({"success": True, "medication": result}), 201
    
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@med_bp.get("/<senior_id>")
def get_medications(senior_id):
    """Get all medications for a senior."""
    try:
        meds = medication_service.get_medications(senior_id)
        return jsonify({"medications": meds}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@med_bp.get("/<senior_id>/today")
def get_today_medications(senior_id):
    """Get medications due today."""
    try:
        meds = medication_service.get_today_medications(senior_id)
        return jsonify({"today_medications": meds}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@med_bp.delete("/<senior_id>/<med_id>")
def delete_medication(senior_id, med_id):
    """Mark medication as inactive."""
    try:
        success = medication_service.delete_medication(senior_id, med_id)
        if success:
            return jsonify({"success": True, "message": "Medication deactivated"}), 200
        else:
            return jsonify({"error": "Medication not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""Safety checks and disclaimers for medical information."""

MEDICAL_DISCLAIMER = """
⚠️ IMPORTANT DISCLAIMER:
This tool is an educational and reminder system only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.

Always consult your doctor before:
- Starting or stopping any medication
- Changing medication dosage
- Taking new medications with existing ones

In case of emergency, call 911 or your local emergency services immediately.
"""

MEDICATION_REMINDER_TEMPLATE = """
💊 MEDICATION REMINDER for {med_name}

Dosage: {dose_quantity} × {dosage}
Frequency: {frequency}
Instructions: {instructions}

⚠️ Always follow your doctor's instructions. If you have questions, contact your healthcare provider.
"""

APPOINTMENT_REMINDER_TEMPLATE = """
📅 APPOINTMENT REMINDER

Doctor: {doctor_name} ({specialization})
Date: {date}
Time: {time}
Location: {location}

Preparation: {notes}

Remember to bring your insurance card and any recent test results.
"""

class SafetyService:
    """Ensures medical information is provided safely."""
    
    @staticmethod
    def format_medication_reminder(med_dict: dict) -> str:
        """Format medication with safety disclaimers."""
        formatted = MEDICATION_REMINDER_TEMPLATE.format(
            med_name=med_dict.get("name", "Unknown"),
            dose_quantity=med_dict.get("dose_quantity", 1),
            dosage=med_dict.get("dosage", ""),
            frequency=med_dict.get("frequency", ""),
            instructions=med_dict.get("instructions", "No special instructions")
        )
        return formatted
    
    @staticmethod
    def format_appointment_reminder(appt_dict: dict) -> str:
        """Format appointment with helpful info."""
        formatted = APPOINTMENT_REMINDER_TEMPLATE.format(
            doctor_name=appt_dict.get("doctor_name", "Unknown"),
            specialization=appt_dict.get("specialization", "General Practice"),
            date=appt_dict.get("date", ""),
            time=appt_dict.get("time", ""),
            location=appt_dict.get("location", "Contact office for details"),
            notes=appt_dict.get("notes", "Arrive 15 minutes early")
        )
        return formatted
    
    @staticmethod
    def add_ai_safety_context(message: str, role: str = "senior") -> str:
        """Add safety context to AI responses."""
        safety_suffix = "\n\n⚠️ This is general information only. Always consult your doctor for medical decisions."
        return message + safety_suffix if role == "senior" else message

safety_service = SafetyService()

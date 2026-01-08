"""Service for managing appointments."""

from ..models import Appointment
from ..backboard_client import add_memory
from datetime import datetime
from typing import List, Optional

class AppointmentService:
    """Business logic for appointment management."""
    
    def __init__(self):
        self.appointments_store = {}
    
    async def save_appointment(self, senior_id: str, appointment: Appointment) -> dict:
        """Save appointment and sync to Backboard memory."""
        if senior_id not in self.appointments_store:
            self.appointments_store[senior_id] = []
        
        appt_dict = appointment.dict()
        appt_dict["appt_id"] = appointment.appt_id or f"appt_{int(datetime.now().timestamp())}"
        self.appointments_store[senior_id].append(appt_dict)
        
        memory_text = f"""
APPOINTMENT RECORD for senior {senior_id}:
- Date: {appointment.date}
- Time: {appointment.time}
- Doctor: {appointment.doctor_name}
- Specialty: {appointment.specialization or 'General'}
- Location: {appointment.location or 'Not specified'}
- Notes: {appointment.notes or 'None'}
- Status: {appointment.status}
"""
        
        try:
            await add_memory(
                content=memory_text,
                metadata={"type": "appointment", "senior_id": senior_id, "appt_id": appt_dict["appt_id"]}
            )
        except Exception as e:
            print(f"Warning: Memory save failed: {e}")
        
        return appt_dict
    
    def get_appointments(self, senior_id: str) -> List[dict]:
        """Get all appointments for a senior."""
        return self.appointments_store.get(senior_id, [])
    
    def get_next_appointment(self, senior_id: str) -> Optional[dict]:
        """Get the next upcoming appointment."""
        appts = self.get_appointments(senior_id)
        if not appts:
            return None
        sorted_appts = sorted(appts, key=lambda a: f"{a['date']} {a['time']}")
        return sorted_appts[0]
    
    def update_appointment(self, senior_id: str, appt_id: str, status: str) -> bool:
        """Update appointment status."""
        if senior_id in self.appointments_store:
            for appt in self.appointments_store[senior_id]:
                if appt.get("appt_id") == appt_id:
                    appt["status"] = status
                    return True
        return False

appointment_service = AppointmentService()

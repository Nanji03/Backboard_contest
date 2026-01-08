"""Pydantic models for request/response validation."""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ============ User Models ============
class SeniorProfile(BaseModel):
    senior_id: str
    name: str
    age: Optional[int] = None
    contact_phone: Optional[str] = None
    doctor_contact: Optional[str] = None
    caregiver_name: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "senior_id": "senior_001",
                "name": "Margaret Johnson",
                "age": 78,
                "contact_phone": "+1-555-0123",
                "doctor_contact": "Dr. Smith, 555-9999",
                "caregiver_name": "John Johnson"
            }
        }

# ============ Medication Models ============
class Medication(BaseModel):
    med_id: Optional[str] = None
    name: str
    dosage: str  # e.g., "500mg"
    dose_quantity: int  # how many tablets/units
    frequency: str  # e.g., "Twice daily", "Morning only"
    instructions: Optional[str] = None  # "Take with food"
    active: bool = True

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Metformin",
                "dosage": "500mg",
                "dose_quantity": 1,
                "frequency": "Twice daily",
                "instructions": "Take with food"
            }
        }

class MedicationSchedule(BaseModel):
    senior_id: str
    medications: List[Medication]

# ============ Appointment Models ============
class Appointment(BaseModel):
    appt_id: Optional[str] = None
    date: str  # ISO format: "2026-01-15"
    time: str  # "14:30"
    doctor_name: str
    specialization: Optional[str] = None  # "Cardiologist"
    location: Optional[str] = None
    notes: Optional[str] = None
    status: str = "scheduled"  # scheduled, completed, cancelled

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-01-15",
                "time": "14:30",
                "doctor_name": "Dr. John Smith",
                "specialization": "Cardiologist",
                "location": "Montreal General Hospital",
                "notes": "Bring recent lab results"
            }
        }

class AppointmentList(BaseModel):
    senior_id: str
    appointments: List[Appointment]

# ============ Report Models ============
class MedicalReport(BaseModel):
    report_id: Optional[str] = None
    senior_id: str
    report_type: str  # "blood_test", "ct_scan", "discharge_summary"
    uploaded_at: str  # ISO datetime
    text_content: str  # The raw text from the report
    summary: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "senior_id": "senior_001",
                "report_type": "blood_test",
                "text_content": "Hemoglobin: 13.5 g/dL. WBC: 7.2...",
                "summary": "Blood test results are normal"
            }
        }

# ============ Chat Models ============
class ChatMessage(BaseModel):
    user_id: str
    role: str  # "senior" or "caregiver"
    message: str
    thread_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "senior_001",
                "role": "senior",
                "message": "What medicine do I take this morning?"
            }
        }

class ChatResponse(BaseModel):
    reply: str
    thread_id: str
    memory_context: Optional[dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "reply": "You should take 1 tablet of Metformin 500mg with breakfast.",
                "thread_id": "thread_123abc"
            }
        }

# ============ Change Request Models ============
class ChangeRequest(BaseModel):
    request_id: Optional[str] = None
    senior_id: str
    medication_id: str
    requested_change: str  # Free text: "Doctor said reduce to once daily"
    visit_date: str  # When was the doctor visit
    status: str = "pending"  # pending, approved, rejected
    created_at: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "senior_id": "senior_001",
                "medication_id": "med_123",
                "requested_change": "Doctor reduced dosage to once daily",
                "visit_date": "2026-01-06"
            }
        }

"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Chat Models
class ChatMessage(BaseModel):
    userId: str
    message: str
    role: str = "senior"  # "senior" or "caregiver"

class ChatResponse(BaseModel):
    message: str
    threadId: str
    role: str
    userId: str
    safe: bool = True
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())

# Medication Models
class Medication(BaseModel):
    id: Optional[str] = None
    name: str
    dose: str
    frequency: str  # "once daily", "twice daily", etc.
    instructions: str = ""
    startDate: Optional[str] = None
    endDate: Optional[str] = None

class MedicationList(BaseModel):
    userId: str
    medications: List[Medication]

class MedicationUpdate(BaseModel):
    medicationId: str
    name: Optional[str] = None
    dose: Optional[str] = None
    frequency: Optional[str] = None
    instructions: Optional[str] = None

# Appointment Models
class Appointment(BaseModel):
    id: Optional[str] = None
    userId: str
    date: str
    time: str
    doctor: str
    reason: str = ""
    notes: Optional[str] = None

class AppointmentUpdate(BaseModel):
    appointmentId: str
    date: Optional[str] = None
    time: Optional[str] = None
    doctor: Optional[str] = None
    reason: Optional[str] = None

# Change Request Models
class ChangeRequest(BaseModel):
    id: Optional[str] = None
    userId: str
    medicationId: str
    changeType: str  # "dose_change", "frequency_change", "new_med", "discontinue"
    doctorNotes: str
    visitDate: str
    status: str = "pending"  # "pending", "approved", "rejected"
    createdAt: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat())

# User/Auth Models
class UserProfile(BaseModel):
    userId: str
    role: str  # "senior", "caregiver", "physician"
    name: str
    email: str
    phone: Optional[str] = None
    emergencyContact: Optional[str] = None

class AuthRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    userId: str
    token: str
    role: str
    expiresIn: int = 3600

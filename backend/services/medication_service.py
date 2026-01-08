"""Service for managing medication schedules."""

from ..models import Medication
from ..backboard_client import add_memory
from datetime import datetime
from typing import List

class MedicationService:
    """Business logic for medication management."""
    
    def __init__(self):
        self.medications_store = {}  # In production, use real database
    
    async def save_medication(self, senior_id: str, medication: Medication) -> dict:
        """Save medication and sync to Backboard memory."""
        if senior_id not in self.medications_store:
            self.medications_store[senior_id] = []
        
        med_dict = medication.dict()
        med_dict["med_id"] = medication.med_id or f"med_{int(datetime.now().timestamp())}"
        self.medications_store[senior_id].append(med_dict)
        
        memory_text = f"""
MEDICATION RECORD for senior {senior_id}:
- Name: {medication.name}
- Dosage: {medication.dosage}
- Quantity: {medication.dose_quantity} units
- Frequency: {medication.frequency}
- Instructions: {medication.instructions or 'None'}
- Status: {'Active' if medication.active else 'Inactive'}
"""
        
        try:
            await add_memory(
                content=memory_text,
                metadata={"type": "medication", "senior_id": senior_id, "med_id": med_dict["med_id"]}
            )
        except Exception as e:
            print(f"Warning: Memory save failed: {e}")
        
        return med_dict
    
    def get_medications(self, senior_id: str) -> List[dict]:
        """Get all medications for a senior."""
        return self.medications_store.get(senior_id, [])
    
    def get_today_medications(self, senior_id: str) -> List[dict]:
        """Get active medications for today."""
        meds = self.get_medications(senior_id)
        return [m for m in meds if m.get("active", True)]
    
    def delete_medication(self, senior_id: str, med_id: str) -> bool:
        """Mark medication as inactive instead of deleting."""
        if senior_id in self.medications_store:
            for med in self.medications_store[senior_id]:
                if med.get("med_id") == med_id:
                    med["active"] = False
                    return True
        return False

medication_service = MedicationService()

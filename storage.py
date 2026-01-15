"""Storage module for appointment data."""

import json
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class AppointmentStorage:
    """Handle appointment data persistence."""
    
    def __init__(self, storage_file: str = "appointments.json"):
        """Initialize storage with file path."""
        self.storage_file = Path(storage_file)
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist."""
        if not self.storage_file.exists():
            self.storage_file.write_text(json.dumps([], indent=2))
    
    def load_appointments(self) -> List[Dict]:
        """Load all appointments from storage."""
        try:
            content = self.storage_file.read_text()
            return json.loads(content) if content else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def save_appointment(self, appointment: Dict) -> bool:
        """Save a new appointment."""
        appointments = self.load_appointments()
        appointment['id'] = len(appointments) + 1
        appointment['created_at'] = datetime.now().isoformat()
        appointments.append(appointment)
        
        try:
            self.storage_file.write_text(json.dumps(appointments, indent=2))
            return True
        except Exception as e:
            print(f"Error saving appointment: {e}")
            return False
    
    def get_appointment(self, appointment_id: int) -> Optional[Dict]:
        """Get a specific appointment by ID."""
        appointments = self.load_appointments()
        for appointment in appointments:
            if appointment.get('id') == appointment_id:
                return appointment
        return None
    
    def update_appointment(self, appointment_id: int, updated_data: Dict) -> bool:
        """Update an existing appointment."""
        appointments = self.load_appointments()
        
        for i, appointment in enumerate(appointments):
            if appointment.get('id') == appointment_id:
                updated_data['updated_at'] = datetime.now().isoformat()
                appointments[i].update(updated_data)
                try:
                    self.storage_file.write_text(json.dumps(appointments, indent=2))
                    return True
                except Exception as e:
                    print(f"Error updating appointment: {e}")
                    return False
        return False
    
    def delete_appointment(self, appointment_id: int) -> bool:
        """Delete an appointment."""
        appointments = self.load_appointments()
        original_length = len(appointments)
        appointments = [a for a in appointments if a.get('id') != appointment_id]
        
        if len(appointments) < original_length:
            try:
                self.storage_file.write_text(json.dumps(appointments, indent=2))
                return True
            except Exception as e:
                print(f"Error deleting appointment: {e}")
                return False
        return False
    
    def get_appointments_by_date(self, date_str: str) -> List[Dict]:
        """Get all appointments for a specific date."""
        appointments = self.load_appointments()
        return [a for a in appointments if a.get('date') == date_str]

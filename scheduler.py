"""Scheduler module for managing appointments."""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from storage import AppointmentStorage


class AppointmentScheduler:
    """Manage appointment scheduling and conflict detection."""
    
    def __init__(self, storage: AppointmentStorage):
        """Initialize scheduler with storage."""
        self.storage = storage
    
    def create_appointment(
        self,
        title: str,
        date: str,
        time: str,
        duration_minutes: int = 60,
        client_name: str = "",
        description: str = ""
    ) -> Dict:
        """Create a new appointment with conflict checking."""
        # Validate date and time format
        try:
            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")
        except ValueError:
            return {"success": False, "error": "Invalid date or time format"}
        
        # Check for conflicts
        conflicts = self._check_conflicts(date, time, duration_minutes)
        if conflicts:
            return {
                "success": False,
                "error": "Appointment conflicts with existing slots",
                "conflicts": conflicts
            }
        
        appointment = {
            "title": title,
            "date": date,
            "time": time,
            "duration_minutes": duration_minutes,
            "client_name": client_name,
            "description": description,
            "status": "scheduled"
        }
        
        success = self.storage.save_appointment(appointment)
        return {
            "success": success,
            "appointment": appointment if success else None
        }
    
    def _check_conflicts(self, date: str, time: str, duration: int) -> List[Dict]:
        """Check for scheduling conflicts."""
        appointments = self.storage.get_appointments_by_date(date)
        conflicts = []
        
        try:
            start_time = datetime.strptime(time, "%H:%M")
            end_time = start_time + timedelta(minutes=duration)
            
            for appt in appointments:
                if appt.get('status') == 'cancelled':
                    continue
                    
                appt_start = datetime.strptime(appt.get('time', ''), "%H:%M")
                appt_end = appt_start + timedelta(minutes=appt.get('duration_minutes', 60))
                
                # Check overlap
                if start_time < appt_end and end_time > appt_start:
                    conflicts.append({
                        "id": appt.get('id'),
                        "title": appt.get('title'),
                        "time": appt.get('time'),
                        "duration": appt.get('duration_minutes')
                    })
        except ValueError:
            pass
        
        return conflicts
    
    def get_available_slots(
        self,
        date: str,
        duration_minutes: int = 60,
        start_hour: int = 9,
        end_hour: int = 17
    ) -> List[str]:
        """Get available time slots for a given date."""
        available_slots = []
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return []
        
        current_time = datetime.strptime(f"{start_hour:02d}:00", "%H:%M")
        end_time = datetime.strptime(f"{end_hour:02d}:00", "%H:%M")
        
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            conflicts = self._check_conflicts(date, time_str, duration_minutes)
            
            if not conflicts:
                available_slots.append(time_str)
            
            current_time += timedelta(minutes=30)
        
        return available_slots
    
    def reschedule_appointment(
        self,
        appointment_id: int,
        new_date: str,
        new_time: str
    ) -> Dict:
        """Reschedule an existing appointment."""
        appointment = self.storage.get_appointment(appointment_id)
        
        if not appointment:
            return {"success": False, "error": "Appointment not found"}
        
        # Check for conflicts at new time
        duration = appointment.get('duration_minutes', 60)
        conflicts = self._check_conflicts(new_date, new_time, duration)
        
        if conflicts:
            return {
                "success": False,
                "error": "New time has conflicts",
                "conflicts": conflicts
            }
        
        success = self.storage.update_appointment(
            appointment_id,
            {"date": new_date, "time": new_time}
        )
        
        return {
            "success": success,
            "message": "Appointment rescheduled successfully" if success else "Failed to reschedule"
        }
    
    def cancel_appointment(self, appointment_id: int) -> Dict:
        """Cancel an appointment."""
        appointment = self.storage.get_appointment(appointment_id)
        
        if not appointment:
            return {"success": False, "error": "Appointment not found"}
        
        success = self.storage.update_appointment(
            appointment_id,
            {"status": "cancelled"}
        )
        
        return {
            "success": success,
            "message": "Appointment cancelled" if success else "Failed to cancel"
        }
    
    def get_day_schedule(self, date: str) -> List[Dict]:
        """Get all appointments for a specific day, sorted by time."""
        appointments = self.storage.get_appointments_by_date(date)
        return sorted(appointments, key=lambda x: x.get('time', ''))
    
    def get_upcoming_appointments(self, days_ahead: int = 7) -> List[Dict]:
        """Get upcoming appointments within specified days."""
        from datetime import datetime, timedelta
        
        appointments = self.storage.load_appointments()
        upcoming = []
        today = datetime.now().date()
        
        for appt in appointments:
            if appt.get('status') == 'cancelled':
                continue
            
            try:
                appt_date = datetime.strptime(appt.get('date', ''), "%Y-%m-%d").date()
                days_diff = (appt_date - today).days
                
                if 0 <= days_diff <= days_ahead:
                    upcoming.append(appt)
            except ValueError:
                continue
        
        return sorted(
            upcoming,
            key=lambda x: (x.get('date', ''), x.get('time', ''))
        )

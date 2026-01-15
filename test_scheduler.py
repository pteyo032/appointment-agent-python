"""Tests for scheduler module."""

import unittest
import tempfile
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scheduler import AppointmentScheduler
from storage import AppointmentStorage


class TestAppointmentScheduler(unittest.TestCase):
    """Test cases for AppointmentScheduler."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = AppointmentStorage(self.temp_file.name)
        self.scheduler = AppointmentScheduler(self.storage)
    
    def tearDown(self):
        """Clean up after tests."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_create_appointment(self):
        """Test creating an appointment."""
        result = self.scheduler.create_appointment(
            title="Test Meeting",
            date="2026-01-15",
            time="10:00",
            duration_minutes=60
        )
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(result['appointment'])
    
    def test_invalid_date_format(self):
        """Test that invalid date format is rejected."""
        result = self.scheduler.create_appointment(
            title="Test",
            date="01-15-2026",  # Wrong format
            time="10:00"
        )
        
        self.assertFalse(result['success'])
        self.assertIn("Invalid", result['error'])
    
    def test_conflict_detection(self):
        """Test that scheduling conflicts are detected."""
        # Create first appointment
        self.scheduler.create_appointment(
            title="Meeting 1",
            date="2026-01-15",
            time="10:00",
            duration_minutes=60
        )
        
        # Try to create overlapping appointment
        result = self.scheduler.create_appointment(
            title="Meeting 2",
            date="2026-01-15",
            time="10:30",
            duration_minutes=60
        )
        
        self.assertFalse(result['success'])
        self.assertIn("conflicts", result)
    
    def test_no_conflict_for_non_overlapping(self):
        """Test that non-overlapping appointments are allowed."""
        self.scheduler.create_appointment(
            title="Meeting 1",
            date="2026-01-15",
            time="10:00",
            duration_minutes=60
        )
        
        result = self.scheduler.create_appointment(
            title="Meeting 2",
            date="2026-01-15",
            time="11:00",
            duration_minutes=60
        )
        
        self.assertTrue(result['success'])
    
    def test_get_available_slots(self):
        """Test getting available time slots."""
        # Create one appointment
        self.scheduler.create_appointment(
            title="Meeting",
            date="2026-01-15",
            time="10:00",
            duration_minutes=60
        )
        
        slots = self.scheduler.get_available_slots("2026-01-15")
        
        self.assertGreater(len(slots), 0)
        self.assertNotIn("10:00", slots)  # Should not be available
        self.assertNotIn("10:30", slots)  # Should not be available
    
    def test_reschedule_appointment(self):
        """Test rescheduling an appointment."""
        self.scheduler.create_appointment(
            title="Meeting",
            date="2026-01-15",
            time="10:00",
            duration_minutes=60
        )
        
        result = self.scheduler.reschedule_appointment(1, "2026-01-16", "14:00")
        
        self.assertTrue(result['success'])
        appt = self.storage.get_appointment(1)
        self.assertEqual(appt['date'], "2026-01-16")
        self.assertEqual(appt['time'], "14:00")
    
    def test_cancel_appointment(self):
        """Test cancelling an appointment."""
        self.scheduler.create_appointment(
            title="Meeting",
            date="2026-01-15",
            time="10:00",
            duration_minutes=60
        )
        
        result = self.scheduler.cancel_appointment(1)
        
        self.assertTrue(result['success'])
        appt = self.storage.get_appointment(1)
        self.assertEqual(appt['status'], 'cancelled')
    
    def test_get_day_schedule(self):
        """Test getting daily schedule."""
        self.scheduler.create_appointment("Meeting 1", "2026-01-15", "09:00", 60)
        self.scheduler.create_appointment("Meeting 2", "2026-01-15", "14:00", 60)
        
        schedule = self.scheduler.get_day_schedule("2026-01-15")
        
        self.assertEqual(len(schedule), 2)
        self.assertEqual(schedule[0]['time'], "09:00")
        self.assertEqual(schedule[1]['time'], "14:00")


if __name__ == '__main__':
    unittest.main()

"""Tests for storage module."""

import unittest
import json
import tempfile
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from storage import AppointmentStorage


class TestAppointmentStorage(unittest.TestCase):
    """Test cases for AppointmentStorage."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.storage = AppointmentStorage(self.temp_file.name)
    
    def tearDown(self):
        """Clean up after tests."""
        Path(self.temp_file.name).unlink(missing_ok=True)
    
    def test_create_storage_file(self):
        """Test that storage file is created."""
        self.assertTrue(Path(self.temp_file.name).exists())
    
    def test_save_and_load_appointment(self):
        """Test saving and loading appointments."""
        appointment = {
            "title": "Test Meeting",
            "date": "2026-01-15",
            "time": "10:00",
            "duration_minutes": 60
        }
        
        self.storage.save_appointment(appointment)
        appointments = self.storage.load_appointments()
        
        self.assertEqual(len(appointments), 1)
        self.assertEqual(appointments[0]['title'], "Test Meeting")
    
    def test_get_appointment(self):
        """Test retrieving specific appointment."""
        appointment = {
            "title": "Doctor Visit",
            "date": "2026-01-20",
            "time": "14:00",
            "duration_minutes": 30
        }
        
        self.storage.save_appointment(appointment)
        retrieved = self.storage.get_appointment(1)
        
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved['title'], "Doctor Visit")
    
    def test_update_appointment(self):
        """Test updating an appointment."""
        appointment = {
            "title": "Meeting",
            "date": "2026-01-15",
            "time": "10:00",
            "duration_minutes": 60
        }
        
        self.storage.save_appointment(appointment)
        self.storage.update_appointment(1, {"title": "Updated Meeting"})
        
        updated = self.storage.get_appointment(1)
        self.assertEqual(updated['title'], "Updated Meeting")
    
    def test_delete_appointment(self):
        """Test deleting an appointment."""
        appointment = {
            "title": "Meeting",
            "date": "2026-01-15",
            "time": "10:00",
            "duration_minutes": 60
        }
        
        self.storage.save_appointment(appointment)
        self.assertTrue(self.storage.delete_appointment(1))
        
        appointments = self.storage.load_appointments()
        self.assertEqual(len(appointments), 0)
    
    def test_get_appointments_by_date(self):
        """Test filtering appointments by date."""
        appt1 = {"title": "Meeting 1", "date": "2026-01-15", "time": "10:00", "duration_minutes": 60}
        appt2 = {"title": "Meeting 2", "date": "2026-01-15", "time": "14:00", "duration_minutes": 60}
        appt3 = {"title": "Meeting 3", "date": "2026-01-16", "time": "10:00", "duration_minutes": 60}
        
        self.storage.save_appointment(appt1)
        self.storage.save_appointment(appt2)
        self.storage.save_appointment(appt3)
        
        result = self.storage.get_appointments_by_date("2026-01-15")
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()

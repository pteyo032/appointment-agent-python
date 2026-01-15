"""Main application for the appointment agent."""

import sys
from datetime import datetime, timedelta
from storage import AppointmentStorage
from scheduler import AppointmentScheduler


class AppointmentAgent:
    """Main agent for managing appointments."""
    
    def __init__(self):
        """Initialize the appointment agent."""
        self.storage = AppointmentStorage("appointments.json")
        self.scheduler = AppointmentScheduler(self.storage)
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("APPOINTMENT AGENT")
        print("="*50)
        print("1. Create new appointment")
        print("2. View appointments")
        print("3. Check available slots")
        print("4. Reschedule appointment")
        print("5. Cancel appointment")
        print("6. View day schedule")
        print("7. View upcoming appointments")
        print("8. Exit")
        print("="*50)
    
    def create_appointment_interactive(self):
        """Create appointment through interactive prompts."""
        print("\n--- Create New Appointment ---")
        
        title = input("Appointment title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return
        
        date = input("Date (YYYY-MM-DD): ").strip()
        time = input("Time (HH:MM): ").strip()
        
        try:
            duration = int(input("Duration (minutes, default 60): ") or "60")
        except ValueError:
            duration = 60
        
        client_name = input("Client name (optional): ").strip()
        description = input("Description (optional): ").strip()
        
        result = self.scheduler.create_appointment(
            title=title,
            date=date,
            time=time,
            duration_minutes=duration,
            client_name=client_name,
            description=description
        )
        
        if result["success"]:
            print(f"\n✓ Appointment created successfully!")
            print(f"  ID: {result['appointment'].get('id')}")
        else:
            print(f"\n✗ Error: {result['error']}")
            if "conflicts" in result:
                print("  Conflicting appointments:")
                for conflict in result["conflicts"]:
                    print(f"    - {conflict['title']} at {conflict['time']}")
    
    def view_all_appointments(self):
        """View all appointments."""
        appointments = self.storage.load_appointments()
        
        if not appointments:
            print("\nNo appointments found.")
            return
        
        print("\n--- All Appointments ---")
        for appt in sorted(appointments, key=lambda x: (x.get('date', ''), x.get('time', ''))):
            status = appt.get('status', 'scheduled')
            if status == 'cancelled':
                continue
            
            print(f"\nID: {appt.get('id')}")
            print(f"  Title: {appt.get('title')}")
            print(f"  Date: {appt.get('date')}")
            print(f"  Time: {appt.get('time')}")
            print(f"  Duration: {appt.get('duration_minutes')} minutes")
            if appt.get('client_name'):
                print(f"  Client: {appt.get('client_name')}")
            if appt.get('description'):
                print(f"  Description: {appt.get('description')}")
    
    def check_available_slots(self):
        """Check available time slots for a date."""
        print("\n--- Check Available Slots ---")
        
        date = input("Date (YYYY-MM-DD): ").strip()
        
        try:
            duration = int(input("Duration (minutes, default 60): ") or "60")
        except ValueError:
            duration = 60
        
        slots = self.scheduler.get_available_slots(date, duration)
        
        if slots:
            print(f"\nAvailable slots for {date}:")
            for slot in slots:
                print(f"  • {slot}")
        else:
            print(f"\nNo available slots for {date} with {duration} minute duration.")
    
    def reschedule_appointment_interactive(self):
        """Reschedule an appointment."""
        print("\n--- Reschedule Appointment ---")
        
        try:
            appt_id = int(input("Appointment ID: "))
        except ValueError:
            print("Invalid ID.")
            return
        
        appointment = self.storage.get_appointment(appt_id)
        if not appointment:
            print("Appointment not found.")
            return
        
        print(f"\nCurrent: {appointment.get('date')} at {appointment.get('time')}")
        
        new_date = input("New date (YYYY-MM-DD): ").strip()
        new_time = input("New time (HH:MM): ").strip()
        
        result = self.scheduler.reschedule_appointment(appt_id, new_date, new_time)
        
        if result["success"]:
            print(f"\n✓ {result['message']}")
        else:
            print(f"\n✗ Error: {result['error']}")
            if "conflicts" in result:
                print("  Conflicting appointments:")
                for conflict in result["conflicts"]:
                    print(f"    - {conflict['title']} at {conflict['time']}")
    
    def cancel_appointment_interactive(self):
        """Cancel an appointment."""
        print("\n--- Cancel Appointment ---")
        
        try:
            appt_id = int(input("Appointment ID to cancel: "))
        except ValueError:
            print("Invalid ID.")
            return
        
        result = self.scheduler.cancel_appointment(appt_id)
        
        if result["success"]:
            print(f"\n✓ {result['message']}")
        else:
            print(f"\n✗ Error: {result['error']}")
    
    def view_day_schedule(self):
        """View schedule for a specific day."""
        print("\n--- Day Schedule ---")
        
        date = input("Date (YYYY-MM-DD): ").strip()
        appointments = self.scheduler.get_day_schedule(date)
        
        if not appointments:
            print(f"\nNo appointments on {date}.")
            return
        
        print(f"\nSchedule for {date}:")
        for appt in appointments:
            status = appt.get('status', 'scheduled')
            if status == 'cancelled':
                continue
            
            print(f"\n  {appt.get('time')} - {appt.get('title')}")
            if appt.get('client_name'):
                print(f"    Client: {appt.get('client_name')}")
            print(f"    Duration: {appt.get('duration_minutes')} minutes")
    
    def view_upcoming(self):
        """View upcoming appointments."""
        print("\n--- Upcoming Appointments ---")
        
        appointments = self.scheduler.get_upcoming_appointments(days_ahead=7)
        
        if not appointments:
            print("\nNo upcoming appointments in the next 7 days.")
            return
        
        print("\nUpcoming appointments (next 7 days):")
        for appt in appointments:
            print(f"\n  {appt.get('date')} at {appt.get('time')} - {appt.get('title')}")
            if appt.get('client_name'):
                print(f"    Client: {appt.get('client_name')}")
    
    def run(self):
        """Run the main application loop."""
        print("\nWelcome to the Appointment Agent!")
        
        while True:
            self.display_menu()
            choice = input("Select option (1-8): ").strip()
            
            if choice == "1":
                self.create_appointment_interactive()
            elif choice == "2":
                self.view_all_appointments()
            elif choice == "3":
                self.check_available_slots()
            elif choice == "4":
                self.reschedule_appointment_interactive()
            elif choice == "5":
                self.cancel_appointment_interactive()
            elif choice == "6":
                self.view_day_schedule()
            elif choice == "7":
                self.view_upcoming()
            elif choice == "8":
                print("\nGoodbye!")
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    agent = AppointmentAgent()
    agent.run()

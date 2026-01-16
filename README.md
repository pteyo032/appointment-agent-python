# Appointment Agent

A Python-based appointment scheduling system that manages bookings, detects conflicts, and provides scheduling assistance.

## Features

- **Create Appointments**: Schedule new appointments with title, date, time, duration, and client information
- **Conflict Detection**: Automatically detects and prevents double-booking
- **Available Slots**: Check free time slots for a given date
- **Reschedule**: Modify existing appointments to new dates/times
- **Cancel**: Cancel appointments when needed
- **Day Schedule**: View all appointments for a specific day
- **Upcoming Appointments**: See appointments for the next 7 days
- **Persistent Storage**: All appointments saved to JSON file

## Project Structure

```
appointment-agent-python/
├── main.py         
├── scheduler.py    
├── storage.py       
├── tests/           
└── README.md        
```

## Usage

### Starting the Application

```bash
python main.py
```

### Interactive Menu

1. **Create new appointment** - Schedule a new appointment
2. **View appointments** - List all appointments
3. **Check available slots** - Find free time slots
4. **Reschedule appointment** - Move appointment to new date/time
5. **Cancel appointment** - Cancel an existing appointment
6. **View day schedule** - See all appointments for a specific day
7. **View upcoming appointments** - See appointments for next 7 days
8. **Exit** - Close the application

### Appointment Fields

- **Title**: Name/description of the appointment
- **Date**: Appointment date (format: YYYY-MM-DD)
- **Time**: Appointment time (format: HH:MM in 24-hour format)
- **Duration**: Length of appointment in minutes (default: 60)
- **Client Name**: Optional name of the client
- **Description**: Optional additional details

## Data Storage

Appointments are stored in `appointments.json` in the following format:

```json
[
  {
    "id": 1,
    "title": "Team Meeting",
    "date": "2026-01-15",
    "time": "10:00",
    "duration_minutes": 60,
    "client_name": "John Doe",
    "description": "Weekly sync",
    "status": "scheduled",
    "created_at": "2026-01-15T09:30:00.000000"
  }
]
```

## Module Overview

### storage.py
Handles all data persistence operations:
- `AppointmentStorage.load_appointments()` - Load all appointments
- `AppointmentStorage.save_appointment()` - Add new appointment
- `AppointmentStorage.get_appointment()` - Retrieve specific appointment
- `AppointmentStorage.update_appointment()` - Modify appointment
- `AppointmentStorage.delete_appointment()` - Remove appointment
- `AppointmentStorage.get_appointments_by_date()` - Filter by date

### scheduler.py
Implements scheduling logic:
- `AppointmentScheduler.create_appointment()` - Create with conflict checking
- `AppointmentScheduler.reschedule_appointment()` - Reschedule with validation
- `AppointmentScheduler.cancel_appointment()` - Cancel appointment
- `AppointmentScheduler.get_available_slots()` - Find free time slots
- `AppointmentScheduler.get_day_schedule()` - View daily schedule
- `AppointmentScheduler.get_upcoming_appointments()` - View upcoming bookings

### main.py
Provides interactive CLI interface with user-friendly menu system.

## Example Usage

### Create an Appointment

```
Appointment title: Doctor Visit
Date (YYYY-MM-DD): 2026-01-20
Time (HH:MM): 14:00
Duration (minutes, default 60): 30
Client name (optional): Jane Smith
Description (optional): Annual checkup

✓ Appointment created successfully!
  ID: 1
```

### Check Available Slots

```
Date (YYYY-MM-DD): 2026-01-20
Duration (minutes, default 60): 60

Available slots for 2026-01-20:
  • 09:00
  • 09:30
  • 10:30
  • 15:00
```

## Future Enhancements

- Email/SMS notifications
- Recurring appointments
- Calendar integration
- Time zone support
- Appointment reminders
- Analytics and reporting
- Multi-user support with authentication

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Overview

<img width="996" height="468" alt="Capture d’écran, le 2026-01-16 à 13 20 54" src="https://github.com/user-attachments/assets/841261fd-fb59-4192-9be0-72c3ab172e5a" />


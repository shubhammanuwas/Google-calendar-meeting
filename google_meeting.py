from datetime import datetime, timedelta
import pytz
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load credentials and create a service object
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "meeting-json"  # Update with your JSON key file

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)
service = build("calendar", "v3", credentials=credentials)

# Define the calendar ID (Use 'primary' for main calendar)
CALENDAR_ID = "shubham.manuwas2@gmail.com"

def check_availability(start_time, end_time):
    """Check if a given time slot is available."""
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time.isoformat(),
        timeMax=end_time.isoformat(),
        singleEvents=True,
        orderBy="startTime",
    ).execute()

    events = events_result.get("items", [])

    if events:
        return False  # Conflict found
    else:
        return True  # No conflict, time slot is available

def book_meeting(start_time, end_time, title="New Meeting"):
    """Book a meeting if the time slot is available, otherwise print 'No'."""
    if check_availability(start_time, end_time):
        event = {
            "summary": title,
            "start": {"dateTime": start_time.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end_time.isoformat(), "timeZone": "Asia/Kolkata"},
        }
        event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"Meeting booked successfully: {event['htmlLink']}")
    else:
        print("No")

# Get user input
date_input = input("Enter date (YYYY-MM-DD): ")
time_input = input("Enter time (HH:MM 24hr format): ")

# Convert user input to datetime object
user_datetime = datetime.strptime(f"{date_input} {time_input}", "%Y-%m-%d %H:%M")
user_datetime = pytz.timezone("Asia/Kolkata").localize(user_datetime)

# Define meeting duration (1 hour)
end_datetime = user_datetime + timedelta(hours=1)

# Try to book the meeting
book_meeting(user_datetime, end_datetime)

import os
import pickle
from datetime import datetime, timedelta, time
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dateutil.parser import parse, ParserError
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']

def initialize_calendar():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service

def preprocess_date(date_str):
    now = datetime.now()
    if "today" in date_str.lower():
        date_str = date_str.lower().replace("today", now.strftime("%Y-%m-%d"))
    elif "tomorrow" in date_str.lower():
        tomorrow = now + timedelta(days=1)
        date_str = date_str.lower().replace("tomorrow", tomorrow.strftime("%Y-%m-%d"))
    return date_str

def parse_date_time(date_str, timezone):
    try:
        # Preprocess the date string to handle "today" and "tomorrow"
        date_str = preprocess_date(date_str)
        
        # Parse the date string
        date_obj = parse(date_str)
        
        # Localize to the specified timezone
        date_obj = timezone.localize(date_obj)
        
        return date_obj
    except (ParserError, ValueError, OverflowError) as e:
        print(f"Error parsing date: {e}")
        return None

def add_event(service):
    event_title = input("Enter event title: ")
    start_date_str = input("Enter start date and time (e.g., 'today 7pm'): ")
    end_date_str = input("Enter end date and time (e.g., 'today 8pm'): ")

    # Set timezone
    timezone = pytz.timezone('Asia/Kolkata')

    # Parse start date
    start_date = parse_date_time(start_date_str, timezone)
    if not start_date:
        print(f"Failed to parse start date: {start_date_str}")
        return

    # Parse end date if provided, otherwise set to 1 hour after start
    if end_date_str:
        end_date = parse_date_time(end_date_str, timezone)
        if not end_date:
            print(f"Failed to parse end date: {end_date_str}")
            return
    else:
        end_date = start_date + timedelta(hours=1)

    event = {
        'summary': event_title,
        'start': {
            'dateTime': start_date.isoformat(),
            'timeZone': str(timezone),
        },
        'end': {
            'dateTime': end_date.isoformat(),
            'timeZone': str(timezone),
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        print(f"Event time: {start_date.strftime('%I:%M %p')} - {end_date.strftime('%I:%M %p')} {timezone}")
    except Exception as e:
        print(f"Failed to create event: {e}")

def list_events(service):
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


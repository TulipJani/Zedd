import os
import pickle
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from dateutil.parser import parse, ParserError
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']
ist = pytz.timezone('Asia/Kolkata')

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
    return date_str.strip()

def parse_date_time(date_str, timezone):
    try:
        date_str = preprocess_date(date_str)
        
        # Remove timezone information if present
        if '+' in date_str:
            date_str = date_str.split('+')[0]
        
        # Parse the date string
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        
        return date_obj
    except (ValueError, OverflowError) as e:
        print(f"Error parsing date: {e}")
        return None
    
def add_event(service):
    event_title = input("Enter event title: ")
    start_date_str = input("Enter start date and time in IST (e.g., '2024-07-12 22:00:00'): ")
    end_date_str = input("Enter end date and time in IST (e.g., '2024-07-12 23:00:00', leave empty for default): ")
    
    # Parse start date
    try:
        ist = pytz.timezone('Asia/Kolkata')
        start_date = ist.localize(datetime.strptime(start_date_str, "%Y-%m-%d %H:%M:%S"))
        start_date_utc = start_date.astimezone(pytz.UTC)
    except ValueError:
        print(f"Failed to parse start date and time: {start_date_str}")
        return
    
    # Parse end date or set default
    if end_date_str:
        try:
            end_date = ist.localize(datetime.strptime(end_date_str, "%Y-%m-%d %H:%M:%S"))
            end_date_utc = end_date.astimezone(pytz.UTC)
        except ValueError:
            print(f"Failed to parse end date and time: {end_date_str}")
            return
    else:
        end_date_utc = start_date_utc + timedelta(hours=1)

    event = {
        'summary': event_title,
        'start': {
            'dateTime': start_date_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_date_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            'timeZone': 'UTC',
        },
    }

    try:
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
        print(f"IST Event time: {start_date.strftime('%Y-%m-%d %I:%M %p')} - {end_date.strftime('%I:%M %p')} IST")
        print(f"UTC Event time: {start_date_utc.strftime('%Y-%m-%d %I:%M %p')} - {end_date_utc.strftime('%I:%M %p')} UTC")
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

def main():
    while True:
        user_input = input("What would you like to do? ").strip().lower()
        
        if user_input.startswith("add event"):
            service = initialize_calendar()
            add_event(service)
        
        elif user_input.startswith("list events") or user_input.startswith("event details"):
            service = initialize_calendar()
            list_events(service)
        
        elif user_input == "quit":
            print("Exiting.")
            break
        
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()

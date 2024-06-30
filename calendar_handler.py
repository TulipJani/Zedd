import os.path
from datetime import datetime, timedelta
import pytz  # Added for timezone handling
import dateparser  # Added for flexible datetime parsing

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# ADD YOUR CALENDAR ID HERE
YOUR_CALENDAR_ID = 'tkjani20@gmail.com'
YOUR_TIMEZONE = 'Asia/Kolkata'  # Your local timezone


def initialize_calendar():
    """Initialize Google Calendar API credentials."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds


def add_event(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        print("Adding new event")
        event_title = input("Enter event title: ")

        # Ask for start time
        start_time_str = input("Enter start time (e.g., 'today 3pm', 'tomorrow 10am'): ")
        start_time = parse_datetime(start_time_str)

        # Ask for end time
        end_time_str = input("Enter end time (leave blank for default 1 hour duration): ")
        if end_time_str.strip():
            end_time = parse_datetime(end_time_str)
        else:
            end_time = start_time + timedelta(hours=1)

        event = {
            'summary': event_title,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': YOUR_TIMEZONE,
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': YOUR_TIMEZONE,
            },
        }

        event = service.events().insert(calendarId=YOUR_CALENDAR_ID, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))

    except HttpError as error:
        print('An error occurred: %s' % error)


def parse_datetime(datetime_str):
    try:
        parsed_datetime = dateparser.parse(datetime_str, settings={'TIMEZONE': YOUR_TIMEZONE, 'RETURN_AS_TIMEZONE_AWARE': True})

        # Adjust parsed datetime if it's a time reference without a specific date
        if parsed_datetime.date() == datetime.now(pytz.timezone(YOUR_TIMEZONE)).date() and parsed_datetime.hour < 12:
            parsed_datetime = parsed_datetime.replace(hour=parsed_datetime.hour + 12)

        if parsed_datetime:
            return parsed_datetime.astimezone(pytz.timezone(YOUR_TIMEZONE))
        else:
            print("Could not parse date/time. Please enter a valid format.")
            return None
    except Exception as e:
        print(f"Error parsing date/time: {e}")
        return None


def list_events(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        print("Getting upcoming events")
        now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        events_result = service.events().list(calendarId=YOUR_CALENDAR_ID,
                                              timeMin=now,
                                              maxResults=10,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        else:
            print('Upcoming events:')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(f"- {event['summary']} (Starts at: {start})")

    except HttpError as error:
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    creds = initialize_calendar()
    while True:
        print("\nOptions:")
        print("1. Add Event to Calendar")
        print("2. List Events")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            add_event(creds)
        elif choice == '2':
            list_events(creds)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

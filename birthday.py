import os
import pickle
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

class CalendarChecker:
    def __init__(self, calendarId) -> None:
        self.service = self.authenticate()
        self.calendarId = calendarId

    def authenticate(self):
        creds = None

        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        return build('calendar', 'v3', credentials=creds)  
    
    def get_all_events(self):
        events_result = self.service.events().list(calendarId=self.calendarId,
                                                   timeMax=(datetime.utcnow() + timedelta(days = 365)).isoformat() + 'Z',
                                                   singleEvents=True,
                                                   maxResults=20,
                                                   orderBy="startTime"
                                                   ).execute()
        return events_result.get('items', [])
    
    def get_all_source_events(self):
        events_result = self.service.events().list(calendarId=self.calendarId).execute()
        return events_result.get('items', [])

    def get_next_events(self, date, limit):
        events_result = self.service.events().list(calendarId=self.calendarId,
                                                   singleEvents=True,
                                                   timeMin=date.isoformat() + 'Z',
                                                   maxResults=limit,
                                                   orderBy="startTime"
                                                   ).execute()
        return events_result.get('items', [])

    def get_event_for_date(self, date):
        events_result = self.service.events().list(calendarId=self.calendarId,
                                            timeMin = date.isoformat() + 'Z',
                                            timeMax = (date + timedelta(seconds=1)).isoformat() + 'Z',
                                            singleEvents = True,
                                            ).execute()
        return events_result.get('items', [])
        
    def get_original_event_from_recurring_event(self, event):
        instances = self.service.events().instances(calendarId=self.calendarId, eventId=event["recurringEventId"], maxResults=1).execute()
        return instances["items"][0]

    
def get_next_day(date):
    return date + timedelta(days=1)

def get_date_string_from_event(event):
    return datetime.fromisoformat(event['start'].get('dateTime', event['start'].get('date'))).strftime('%A, %d. %B %Y')

if __name__ == '__main__':
    from config import Config
    config = Config()

    CalendarChecker = CalendarChecker(config.calendarId)
    now = datetime.utcnow()
    all = CalendarChecker.get_all_events()
    limit = 5
    events = CalendarChecker.get_next_events(now, limit)
    today = CalendarChecker.get_event_for_date(now)
    
    print(now)
    print(get_next_day(now))
    print()

    print("todays e")
    for e in today:
        print(f"{e['summary']} - {get_date_string_from_event(e)}")

    print("")
    print(f"next {limit} e")

    for e in events:
        print(f"{e['summary']} - {get_date_string_from_event(e)}")

    print("")
    for e in all:
        if "recurringEventId" in e:
            print(f"recurring {e['recurringEventId']} - {e['summary']} - {get_date_string_from_event(e)} - originally {get_date_string_from_event(CalendarChecker.get_original_event_from_recurring_event(e))}")
        else:
            print(f"one-off {e['id']} - {e['summary']} - {get_date_string_from_event(e)}")
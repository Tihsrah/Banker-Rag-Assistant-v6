# from datetime import datetime, timedelta
# from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials

# def create_meeting(banker_email, title, description, start_time, duration_minutes=30, token_path='token.json'):
#     creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/calendar.events'])
#     service = build('calendar', 'v3', credentials=creds)

#     end_time = start_time + timedelta(minutes=duration_minutes)

#     event = {
#         'summary': title,
#         'description': description,
#         'start': {
#             'dateTime': start_time.isoformat(),
#             'timeZone': 'Asia/Kolkata',
#         },
#         'end': {
#             'dateTime': end_time.isoformat(),
#             'timeZone': 'Asia/Kolkata',
#         },
#         'attendees': [
#             {'email': banker_email}
#         ],
#         'reminders': {
#             'useDefault': True,
#         },
#     }

#     try:
#         event_result = service.events().insert(calendarId='primary', body=event).execute()
#         return {
#             'status': 'success',
#             'event_link': event_result.get('htmlLink')
#         }
#     except Exception as e:
#         return {
#             'status': 'error',
#             'error': str(e)
#         }

# import os
# import uuid
# from datetime import datetime, timedelta

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# SCOPES = ['https://www.googleapis.com/auth/calendar']

# def authenticate_calendar():
#     creds = None
#     token_file = 'token_calendar.json'

#     if os.path.exists(token_file):
#         creds = Credentials.from_authorized_user_file(token_file, SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('client_calender_secret.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         with open(token_file, 'w') as token:
#             token.write(creds.to_json())

#     return build('calendar', 'v3', credentials=creds)

# def create_meeting(banker_email, title, description, start_time, duration_minutes=30):
#     try:
#         service = authenticate_calendar()

#         end_time = start_time + timedelta(minutes=duration_minutes)
#         event = {
#             'summary': title,
#             'description': description,
#             'start': {
#                 'dateTime': start_time.isoformat(),
#                 'timeZone': 'Asia/Kolkata'
#             },
#             'end': {
#                 'dateTime': end_time.isoformat(),
#                 'timeZone': 'Asia/Kolkata'
#             },
#             'attendees': [{'email': banker_email}],
#             'conferenceData': {
#                 'createRequest': {
#                     'requestId': str(uuid.uuid4()),
#                     'conferenceSolutionKey': {'type': 'hangoutsMeet'}
#                 }
#             }
#         }

#         event = service.events().insert(
#             calendarId='primary',
#             body=event,
#             conferenceDataVersion=1
#         ).execute()

#         return {
#             "status": "success",
#             "event_link": event.get("htmlLink"),
#             "meet_link": event.get("hangoutLink")
#         }
#     except Exception as e:
#         return {"status": "error", "error": str(e)}

import os
import uuid
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API scope
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Resolve file paths relative to this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, 'token_calendar.json')
CLIENT_SECRET_PATH = os.path.join(BASE_DIR, 'client_calender_secret.json')

def authenticate_calendar():
    """
    Authenticates and returns a Google Calendar API service using persistent tokens.
    """
    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def create_meeting(banker_email, title, description, start_time, duration_minutes=30):
    """
    Creates a Google Calendar event with a Meet link and returns relevant metadata.
    """
    try:
        service = authenticate_calendar()
        end_time = start_time + timedelta(minutes=duration_minutes)

        event = {
            'summary': title,
            'description': description,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
            'attendees': [{'email': banker_email}],
            'conferenceData': {
                'createRequest': {
                    'requestId': str(uuid.uuid4()),
                    'conferenceSolutionKey': {'type': 'hangoutsMeet'}
                }
            }
        }

        created_event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        return {
            "status": "success",
            "event_id": created_event["id"],
            "event_link": created_event.get("htmlLink", ""),
            "meet_link": created_event.get("hangoutLink", "")
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

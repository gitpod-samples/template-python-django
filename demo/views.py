from django.shortcuts import render, HttpResponse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from .models import demoModel
import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']
# Create your views here.

event1 = {
    'summary': 'TEst meet',
    'location': 'Jehanabad',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': datetime.datetime(2022, 10, 23, 10, 30, 00).isoformat(),
        'timeZone': 'Asia/Kolkata',
    },
    'end': {
        'dateTime': datetime.datetime(2022, 10, 23, 11, 15, 00).isoformat(),
        'timeZone': 'Asia/Kolkata',
    },
    'attendees': [
        {'email': 'adityaprakashgupta726@gmail.com', 'displayName' : 'Aditya Prakash'},
    ],
    # SecureRandom.uuid
    "conferenceData": {"createRequest": {"requestId": "SecureRandom.uuid",
                                         "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
}


def demoview(request):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if demoModel.objects.all():
        print("from db")
        creds = demoModel.objects.all()[0].crds
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("expired")
            creds.refresh(Request())
        else:
            # flow = InstalledAppFlow.from_client_secrets_file(
            #     'credentials.json', SCOPES)
            flow = InstalledAppFlow.from_client_config({"installed": {"client_id": "815661547899-5orlibqmtcosbjo29b540gjjfph2o68q.apps.googleusercontent.com", "project_id": "optimal-pursuit-272105", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                                                       "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_secret": "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"}}, SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        obj = demoModel.objects.create(crds=creds)
        obj.save()

    try:
        service = build('calendar', 'v3', credentials=creds)
    # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print(now)
        print('Getting the upcoming 10 events')
        # en.indian#holiday@group.v.calendar.google.com
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=11, singleEvents=True,
                                              orderBy='startTime').execute()
        # cld = service.calendarList().list().execute()
        # x = service.events().insert(calendarId="primary", sendNotifications=True, body=event1, conferenceDataVersion=1).execute()
        x = service.events().insert(calendarId="primary", body=event1, conferenceDataVersion=1).execute()
        print(x)
        events = events_result.get('items', [])
        # print(cld)

        if not events:
            print('No upcoming events found.')

        # Prints the start and name of the next 10 events
        st = ""
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            st += start + " " + event['summary'] + "<br>"
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)
    return HttpResponse(st)

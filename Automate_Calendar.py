from __future__ import print_function

import datetime
import os.path

from dateutil import parser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
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
    commitHours(creds)
    addEvent(creds, 2, "LeetCode Time")

def commitHours(creds):
    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        today = datetime.date.today()
        timeStart = str(today) + "T05:00:00Z"  # 'Z' represents UTC time
        timeEnd = str(today) + "T23:59:59Z"    
        print("Getting today's total hours spent on lectures and assignment")
        
        events_result = service.events().list(
            calendarId='primary', # change according to calendar you want to track
            timeMin = timeStart, timeMax = timeEnd, singleEvents=True,
            orderBy='startTime', timeZone = 'America/Toronto').execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        total_duration = datetime.timedelta(
        seconds = 0,
        minutes = 0,
        hours = 0,
        )

        id = 0
        print ("Total Hours Spent on Lectures and Assignments: ")
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            start_formatted = parser.isoparse(start)  # changing the start time to datetime format.
            end_formatted = parser.isoparse(end)  # changing the end time to datetime format.
            duration = end_formatted - start_formatted

            total_duration += duration
            print (f"{event['summary']}, duration: {duration}")
        print(f"Total Hours Spent on Lectures and Assignments: {total_duration}")


   
    except HttpError as error:
        print('An error occurred: %s' % error)
        

# function to add calendar event from current time for length [duration].

def addEvent(creds, duration, description):
    start = datetime.datetime.utcnow()
    
    end = datetime.datetime.utcnow() + datetime.timedelta(hours=int(duration))
    start_formatted = start.isoformat() + 'Z'
    end_formatted = end.isoformat() + 'Z'

    event = {
    'summary': description,
    'start': {
        'dateTime': start_formatted,
        'timeZone': 'America/Toronto',
        },
    'end': {
        'dateTime': end_formatted,
        'timeZone': 'America/Toronto',
        },
    }

    service = build('calendar', 'v3', credentials=creds)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))



if __name__ == '__main__':
    main()

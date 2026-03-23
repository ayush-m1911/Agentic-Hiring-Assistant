import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class InterviewSchedulerAgent:
    def __init__(self):
        self.creds = None
        if os.path.exists("token.pkl"):
            with open("token.pkl", "rb") as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret_397715828389-vpc9m9h13sa8jgq9fmk92od5sniaet3a.apps.googleusercontent.com.json", SCOPES
                ) # browser open krta , google permission deta , token save hota#
                self.creds = flow.run_local_server(port=0)

            with open("token.pkl", "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("calendar", "v3", credentials=self.creds) # client object talks with calendar

    def schedule_interview(self, candidate_email, start_time, end_time):
        event = {
            "summary": "Technical Interview",
            "description": "Interview scheduled via Agentic Hiring Assistant",
            "start": {
                "dateTime": start_time,
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": end_time,
                "timeZone": "Asia/Kolkata",
            },
            "attendees": [{"email": candidate_email}],
            "conferenceData": {
                "createRequest": {
                    "requestId": f"meet-{datetime.datetime.now().timestamp()}"
                }
            },
        } # event is created #

        created_event = self.service.events().insert(
            calendarId="primary",
            body=event,
            conferenceDataVersion=1
        ).execute()
        # creates meet link and associated it with event #

        return {
            "meet_link": created_event.get("hangoutLink"),
            "start": start_time,
            "end": end_time
        }
        # return meet link and time details #
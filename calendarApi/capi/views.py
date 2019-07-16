from __future__ import print_function
import datetime   
import pytz
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Availabledata,Userdata

def import_data(request):
    scopes = ['https://www.googleapis.com/auth/calendar']
    credentials = pickle.load(open("token.pkl", "rb"))

    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary',
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        return redirect('/admin/capi/availabledata')
    for event in events:
        existing_event=Availabledata.objects.filter(event_id = event['id']).count()
        if (existing_event==0):
            if event['summary'] == 'Available':
                user=Userdata.objects.get(personal_email=event['creator']['email'])
                new_record = Availabledata.objects.create(event_id=event['id'],
                userID=user,
                available_end_time=event['end']['dateTime'],
                available_start_time=event['start']['dateTime']
                )
    return redirect('/admin/capi/availabledata')
from __future__ import print_function
import datetime   
import pickle
from googleapiclient.discovery import build
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
        if non_existing_event(event['id']):
            if event['summary'] == 'Available':
                user=Userdata.objects.get(personal_email=event['creator']['email'])
                new_record = Availabledata.objects.create(event_id=event['id'],
                userID=user,
                available_end_time=event['end']['dateTime'],
                available_start_time=event['start']['dateTime']
                )
    return redirect('/admin/capi/availabledata')

def non_existing_event(id):
    existing_event=Availabledata.objects.filter(event_id = id).count()
    return existing_event == 0

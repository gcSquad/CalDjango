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
    # timemin=datetime.datetime.now()-datetime.timedelta(days='1')
    service = build('calendar', 'v3', credentials=credentials)
    events_result = service.events().list(calendarId='primary',
                                         singleEvents=True,
                                         timeMin="2018-07-03T14:30:00+03:00",
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    event_in_db =list(Availabledata.objects.values_list('event_id',flat=True))
    users_in_db =list(Userdata.objects.all())
    user_email_list=[]
    for users in users_in_db:
        user_email_list.append(users.personal_email)
        new_records=[]
    for event in events:
        if  event['id'] not in event_in_db and event['creator']['email'] in user_email_list:
            user=return_userby_email(event['creator']['email'],users_in_db)
            new_records.append(event_id=event['id'],
            userID=user,
            available_end_time=event['end']['dateTime'],
            available_start_time=event['start']['dateTime']
            )
            Availabledata.objects.bulk_create(new_records)
        
            
    return redirect('/admin/capi/availabledata')

def check_users_email(email,userlist):
    for user in userlist:
        if(user.personal_email == email):
            return True
        else:
            continue

def return_userby_email(email,userlist):
    for user in userlist:
        if(user.personal_email == email):
            return user
        else:
            continue

                

    

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from tasks import setappointment
import datetime   
import pickle
import os.path
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from django.core.files import File
import json

class Userdata(models.Model):
    userID = models.AutoField(primary_key=True)
    personal_email=  models.EmailField(max_length=70,blank=True, null= True, unique= True)
    Username = models.CharField(max_length=120)
    
    def __str__(self):
        return self.Username

class Availabledata(models.Model):
    userID=models.ForeignKey(Userdata)
    available_start_time =models.DateTimeField()
    available_end_time =models.DateTimeField()
    event_id = models.CharField(max_length=100,blank=True)

    @classmethod
    def return_userby_email(self,email,userlist):
        for user in userlist:
            if(user.personal_email == email):
                return user
            else:
                continue
#"2018-07-03T14:30:00+03:00"


    @classmethod
    def get_event_data(self):
        scopes = ['https://www.googleapis.com/auth/calendar']
        credentials = pickle.load(open("token.pkl", "rb"))
        tz = pytz.timezone('Asia/Kolkata')
        previous_datetime=datetime.datetime.now()-datetime.timedelta(days=1)
        timemin=tz.localize(previous_datetime).replace(microsecond=0).isoformat()
        next_datetime=datetime.datetime.now()+datetime.timedelta(days=1)
        timeMax=tz.localize(next_datetime).replace(microsecond=0).isoformat()
        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary',
                                            singleEvents=True,
                                            timeMin=timemin,
                                            timeMax=timeMax,
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
                user=self.return_userby_email(event['creator']['email'],users_in_db)
                new_object=self(event_id=event['id'],userID=user,available_end_time=event['end']['dateTime'],available_start_time=event['start']['dateTime'])
                new_records.append(new_object)
        self.objects.bulk_create(new_records)
        return

    

    def __str__(self):
        return self.userID.personal_email


class Assignementdata(models.Model):
    userID=models.ForeignKey(Userdata)
    assigned_start_time =models.DateTimeField()
    assigned_end_time =models.DateTimeField()
    event_id = models.CharField(max_length=100,blank=True)

    def save_calendar_event(self):
        event=self.insert_api_call()
        self.event_id=event['id']
        self.save(test_flag=True)

    def insert_api_call(self):
        email=self.userID.personal_email
        start_time=self.assigned_start_time.isoformat()
        end_time=self.assigned_end_time.isoformat()

        scopes = ['https://www.googleapis.com/auth/calendar']
        if os.path.exists("token.pkl"):
            credentials = pickle.load(open("token.pkl", "rb"))
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=scopes)
            credentials = flow.run_console()
            pickle.dump(credentials, open("token.pkl", "wb"))
        
        service = build("calendar", "v3", credentials=credentials)

        event = {
            'summary': 'Meeting Sceduled',
            'description': 'Time for work.',
            'start': {
                'dateTime': start_time,
                "TimeZone": "Asia/Kolkata", 
            },
            'end': {
                'dateTime': end_time,
                "TimeZone": "Asia/Kolkata",   
            },
            'attendees': [
                {'email': email},
            ],
            }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return event


    def validate_entered_time(self):
        return self.assigned_end_time > self.assigned_start_time
            

    def check_user_availability(self):
        valid_time = self.validate_entered_time()
        if valid_time:
            available_record= Availabledata.objects.filter(userID__userID=self.userID.userID)
            count =available_record.count()
            for i in range(count):
                return (self.assigned_start_time >= available_record[i].available_start_time and self.assigned_end_time < available_record[i].available_end_time)

    def save(self,*args,**kwargs):
        user_available = self.check_user_availability()
        if user_available:
            if 'test_flag' in kwargs:
                del kwargs['test_flag']
                super(Assignementdata,self).save(*args,**kwargs)
            else:
                super(Assignementdata,self).save(*args,**kwargs)
                transaction.on_commit(lambda:setappointment.delay(self.id))
        else:
            print("The timeslots entered is not correct for given user")

        
        
        




    



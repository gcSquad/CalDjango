# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from tasks import setappointment
import datetime   
import pickle
import os.path
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

    def __str__(self):
        return self.userID.personal_email


        

class Assignementdata(models.Model):
    userID=models.ForeignKey(Userdata)
    assigned_start_time =models.DateTimeField()
    assigned_end_time =models.DateTimeField()
    event_id = models.CharField(max_length=100,blank=True)
    def save_calendar_event(self):

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
        self.event_id=event['id']
        self.save(test_flag=True)



    def save(self,*args,**kwargs):

        isa_email_id=(self.userID.personal_email)
        available_record=Availabledata.objects.filter(userID__userID=self.userID.userID)
        count=available_record.count()
        for i in range(count):  
            if(self.assigned_start_time >= available_record[i].available_start_time and self.assigned_end_time <available_record[i].available_end_time):
                if 'test_flag' in kwargs and kwargs["test_flag"] == True:
                    super(Assignementdata,self).save(*args,**kwargs)
                else:
                    setappointment.delay(self.id)
                    
            else:
                print("User is not available for the given timeslot")
        
        
        




    



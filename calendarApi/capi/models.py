# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from tasks import setappointment
import datetime   
import pickle
import os.path
import pytz
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from django.contrib.postgres.fields import JSONField
from django.core.files import File
import json
from django.db import transaction
from google.oauth2.credentials import Credentials

class CredentialsDB(models.Model):

    token=models.CharField(max_length=500,null=True,blank=True)
    refresh_token=models.CharField(max_length=500,null=True,blank=True)
    client_secret=models.CharField(max_length=500,null=True,blank=True)
    client_id=models.CharField(max_length=500,null=True,blank=True)
    user_email=  models.EmailField(max_length=70,default="gaurav.chaturvedi@squadrun.co")
    client_secret_file=JSONField()

    
    @classmethod
    def get_credentials(self,email):

        Credentials_data=CredentialsDB.objects.get(user_email=email)
        credentials={
            "token":Credentials_data.token,
            "refresh_token":Credentials_data.refresh_token,
            "client_secret":Credentials_data.client_secret,
            "client_id":Credentials_data.client_id,
            "token_uri":"https://oauth2.googleapis.com/token"
        }
        cred_obj= Credentials(**credentials)
        return cred_obj

    @classmethod
    def save_new_credential(self,email):
        scopes = ['https://www.googleapis.com/auth/calendar']
        try:
            client_data=CredentialsDB.objects.get(user_email=email)
            print(client_data)
            client_secret_data=client_data.client_secret_file
            print("json",client_secret_data)
        except CredentialsDB.DoesNotExist:
            print("have to figure out what to do yha p")
        print("flow started")
        flow = InstalledAppFlow.from_client_config(client_secret_data, scopes=scopes)
        credentials = flow.run_local_server()
        # new_credential= CredentialsDB.objects.create(user_email=email,token=credentials.token,refresh_token=credentials.refresh_token,client_id=credentials.client_id,client_secret=credentials.client_secret)
        new_credential,created= CredentialsDB.objects.update_or_create(user_email=email,token=credentials.token,refresh_token=credentials.refresh_token,client_id=credentials.client_id,client_secret=credentials.client_secret,client_secret_file=client_secret_data)
        
        # new_credential.save()


    
class Userdata(models.Model):
    userID = models.AutoField(primary_key=True,db_column="userID")
    personal_email=  models.EmailField(max_length=70, unique= True)
    Username = models.CharField(max_length=120)
    
    def __unicode__(self):
        return self.Username

class Availabledata(models.Model):
    userID=models.ForeignKey(Userdata)
    available_start_time =models.DateTimeField()
    available_end_time =models.DateTimeField()
    event_id = models.CharField(max_length=100,blank=True,null=True)

    @classmethod
    def return_userby_email(self,email,userlist):
        for user in userlist:
            if(user.personal_email == email):
                return user
    @classmethod
    def return_dates(self,days_delta,operator):

        tz = pytz.timezone('Asia/Kolkata')
        if operator == 'add':
            required_datetime = datetime.datetime.now()+datetime.timedelta(days=days_delta)
        elif operator == 'subtract':
            required_datetime = datetime.datetime.now()-datetime.timedelta(days=days_delta)

        date_in_required_format = tz.localize(required_datetime).replace(microsecond=0).isoformat()
        return date_in_required_format

    @classmethod
    def event_data(self,email):
        
        try:
            user_exist= CredentialsDB.objects.get(user_email=email)
        except CredentialsDB.DoesNotExist:
            CredentialsDB.save_new_credential(email)
        if not user_exist.token:
            CredentialsDB.save_new_credential(email)

        cred_obj= CredentialsDB.get_credentials(email)
        timemin = self.return_dates(10,'subtract')
        timeMax = self.return_dates(10,'add') 
        service = build('calendar', 'v3', credentials=cred_obj)

        events_result = service.events().list(calendarId='primary',singleEvents=True,timeMin=timemin,timeMax=timeMax,orderBy='startTime').execute()

        events = events_result.get('items', [])
        event_in_db =list(Availabledata.objects.values_list('event_id',flat=True))
        users_in_db =list(Userdata.objects.all())
        user_email_list=[]
        new_records=[]
        for users in users_in_db:
            user_email_list.append(users.personal_email)   
        for event in events:
             if  event['id'] not in event_in_db and event['creator']['email'] in user_email_list:
                user=self.return_userby_email(event['creator']['email'],users_in_db)
                new_object= self(event_id=event['id'],userID=user,
                                available_end_time=event['end']['dateTime'],
                                available_start_time=event['start']['dateTime']
                                )

                new_records.append(new_object)
        self.objects.bulk_create(new_records)
        return

    

    def __unicode__(self):
        return self.userID.personal_email


class Assignementdata(models.Model):
    userID=models.ForeignKey(Userdata,db_column="userID")
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
        credentials = CredentialsDB.get_credentials(email)
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
            
            count =available_record.count() #get total records for a particular isa
            
            for i in range(count):       #check if isa's available slot fits for asignement 

                slot_available_start_time = available_record[i].available_start_time
                slot_available_end_time = available_record[i].available_end_time

                return (self.assigned_start_time >= slot_available_start_time and self.assigned_end_time < slot_available_end_time)

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

        
        
        




    



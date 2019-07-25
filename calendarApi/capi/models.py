# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from tasks import setappointment
import datetime   
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from django.contrib.postgres.fields import JSONField
from django.core.files import File
from django.urls import reverse
import json
from django.core.exceptions import ValidationError
from django.db import transaction
from google.oauth2.credentials import Credentials
from django.conf import settings
from utils import return_dates_in_isoformat

class Credential(models.Model):

    token=models.CharField(max_length=500,null=True,blank=True)
    refresh_token=models.CharField(max_length=500,null=True,blank=True)
    user_email=  models.EmailField(max_length=70,unique=True)
    client_secret_file=JSONField()
    state=models.CharField(max_length=500,null=True,blank=True)

    class Meta:
        verbose_name_plural = "Credentials"

    def get_credentials(self):
        credentials={
            "token":self.token,
            "refresh_token":self.refresh_token,
            "client_secret":self.client_secret_file["web"]["client_secret"],
            "client_id":self.client_secret_file["web"]["client_id"],
            "token_uri":self.client_secret_file["web"]["token_uri"]
        }
        cred_obj= Credentials(**credentials)
        return cred_obj
 
    def return_auth_url(self):
        scopes = ['https://www.googleapis.com/auth/calendar']

        client_secret_data=self.client_secret_file
        flow = InstalledAppFlow.from_client_config(client_secret_data, scopes=scopes)
        flow.redirect_uri= settings.AUTH_REDIRECT_URI+reverse('capture_token')
        auth_url_and_state = flow.authorization_url(access_type="offline",prompt="consent")

        self.state = auth_url_and_state[1]
        self.save()

        return auth_url_and_state[0]

    def import_fresh_available_data(self):

        credential_object= self.get_credentials()
        events = self.get_all_events_for_admin(credential_object)
        
        return events

    def get_all_events_for_admin(self,credential_object):
        
        time_min = return_dates_in_isoformat(2,'subtract')
        time_max = return_dates_in_isoformat(2,'add') 

        service = build('calendar', 'v3', credentials=credential_object)
        events_result = service.events().list(calendarId='primary',singleEvents=True,timeMin=time_min,timeMax=time_max,orderBy='startTime').execute()

        events = events_result.get('items', [])
        return events

    @classmethod
    def save_captured_token(cls,state,code,email):
        scopes = ['https://www.googleapis.com/auth/calendar']

        client_data=Credential.objects.get(state=state)
        client_secret_data=client_data.client_secret_file
        flow = InstalledAppFlow.from_client_config(client_secret_data, scopes=scopes)
        flow.redirect_uri= settings.AUTH_REDIRECT_URI+reverse('capture_token')
        
        recieved_token=flow.fetch_token(code=code)

        new_credential,created = Credential.objects.update_or_create(user_email=email,
        client_secret_file = client_secret_data,defaults={"token":recieved_token["access_token"],"refresh_token":recieved_token["refresh_token"]})

    



            
class UserData(models.Model):
    userID = models.AutoField(primary_key=True,db_column="userID")
    personal_email=  models.EmailField(max_length=70, unique= True)
    Username = models.CharField(max_length=120)
    
    class Meta:
        verbose_name_plural = "users"

    def __unicode__(self):
        return self.Username

class AvailableData(models.Model):
    user=models.ForeignKey(UserData)
    available_start_time =models.DateTimeField()
    available_end_time =models.DateTimeField()
    event_id = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        verbose_name_plural = "availableData"
                
    @classmethod
    def save_new_events_db(cls,events):
        total_event_list =list(AvailableData.objects.values_list('event_id',flat=True))
        users_in_db =list(UserData.objects.all())
        user_email_list={}
        new_records=[]

        for users in users_in_db:
            user_email_list.update({users.personal_email:users}) 
              
        for event in events:
             if  event['id'] not in total_event_list and event['creator']['email'] in user_email_list:
                user=user_email_list[event['creator']['email']]
                new_object= cls(event_id=event['id'],user=user,
                                available_end_time=event['end']['dateTime'],
                                available_start_time=event['start']['dateTime']
                                )

                new_records.append(new_object)
        cls.objects.bulk_create(new_records)

    

    def __unicode__(self):
        return self.user.personal_email


class AssignementData(models.Model):
    user=models.ForeignKey(UserData)
    assigned_start_time =models.DateTimeField()
    assigned_end_time =models.DateTimeField()
    event_id = models.CharField(max_length=100,blank=True)

    class Meta:
        verbose_name_plural = "assignmentData"

    def save_appointment(self):

        event=self.get_appointment_event()
        self.event_id=event['id']

        self.save(test_flag=True)

    def get_appointment_event(self):

        email=self.user.personal_email
        start_time=self.assigned_start_time.isoformat()
        end_time=self.assigned_end_time.isoformat()

        scopes = ['https://www.googleapis.com/auth/calendar']
        credentials = Credential.objects.get(user_email=email).get_credentials()
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
            

    def check_user_availability(self):
        valid_count=0
        if self.assigned_end_time > self.assigned_start_time:

            available_record= AvailableData.objects.filter(user__userID=self.user.userID)
            count = available_record.count() #get total records for a particular isa
            
            for i in range(count): #check if isa's available slot fits for asignement 

                slot_available_start_time = available_record[i].available_start_time
                slot_available_end_time = available_record[i].available_end_time
                
                if self.assigned_start_time >= slot_available_start_time and self.assigned_end_time < slot_available_end_time:
                    valid_count =valid_count+1

            return valid_count >0

    def clean(self):
        user_available = self.check_user_availability()
        if not user_available:
            raise ValidationError(('Selected User is not available for given time slot!!'))


    def save(self,*args,**kwargs):

        user_available = self.check_user_availability()
        if user_available:
            if 'test_flag' in kwargs:
                del kwargs['test_flag']
                super(AssignementData,self).save(*args,**kwargs)
            else:
                super(AssignementData,self).save(*args,**kwargs)
                transaction.on_commit(lambda:setappointment.delay(self.id))
        

        
        
        




    



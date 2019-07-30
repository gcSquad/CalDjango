# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
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

        flow = InstalledAppFlow.from_client_config(self.client_secret_file, scopes=settings.AUTH_SCOPE)
        flow.redirect_uri= settings.AUTH_REDIRECT_URI+reverse('capture_token')
        auth_url,state = flow.authorization_url(access_type="offline",prompt="consent")

        self.state = state
        self.save(update_fields=["state"])

        return auth_url

    def get_fresh_available_data(self):

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

        client_data=Credential.objects.get(state=state)

        flow = InstalledAppFlow.from_client_config(client_data.client_secret_file, scopes=settings.AUTH_SCOPE)
        flow.redirect_uri= settings.AUTH_REDIRECT_URI+reverse('capture_token')
        recieved_token=flow.fetch_token(code=code)

        client_data.token=recieved_token["access_token"]
        client_data.refresh_token=recieved_token["refresh_token"]
        client_data.save(update_fields=["token","refresh_token"])

            
class UserData(models.Model):
    user = models.AutoField(primary_key=True,db_column="userID")
    personal_email=  models.EmailField(max_length=70, unique= True)
    username = models.CharField(max_length=120)
    
    class Meta:
        verbose_name_plural = "users"

    def __unicode__(self):
        return self.username

class AvailableData(models.Model):
    user=models.ForeignKey(UserData)
    available_start_time =models.DateTimeField()
    available_end_time =models.DateTimeField()
    event_id = models.CharField(max_length=100,blank=True,null=True)

    class Meta:
        verbose_name_plural = "availableData"

    def __unicode__(self):
        return self.user.personal_email

                
    @classmethod
    def save_new_events_in_db(cls,events):

        existing_event_id_list = list(AvailableData.objects.values_list('event_id',flat=True))
        email_vs_user_object_map =dict(UserData.objects.values_list('personal_email','user'))
        new_available_data_objects=[]

        for event in events:

             if  event['id'] not in existing_event_id_list and event['creator']['email'] in email_vs_user_object_map:
                 
                user=email_vs_user_object_map[event['creator']['email']]
                new_available_object= cls(event_id=event['id'],user_id=user,
                                available_end_time=event['end']['dateTime'],
                                available_start_time=event['start']['dateTime']
                                )

                new_available_data_objects.append(new_available_object)
        cls.objects.bulk_create(new_available_data_objects)   

    

class AssignementData(models.Model):
    
    user=models.ForeignKey(UserData)
    assigned_start_time =models.DateTimeField()
    assigned_end_time =models.DateTimeField()
    event_id = models.CharField(max_length=100,blank=True)

    class Meta:
        verbose_name_plural = "assignmentData"

    def clean(self):
        user_available = self.check_user_availability()
        if not user_available:
            raise ValidationError(('Selected User is not available for given time slot!!'))

    def save_appointment_to_calendar(self,logged_in_user_email):
        
        event = self.create_appointment_event(logged_in_user_email)

        if not self.event_id:
            self.event_id=event['id']
            self.save(update_fields=["event_id"])


    def create_appointment_event(self,logged_in_user_email):

        player_email=self.user.personal_email
        start_time = self.assigned_start_time.isoformat()
        end_time = self.assigned_end_time.isoformat()

        credentials = Credential.objects.get(user_email=logged_in_user_email).get_credentials()
        service = build("calendar", "v3", credentials=credentials)
        event = {
            'summary': 'Meeting Scheduled',
            'description': 'Time for work.',
            'start': {
                'dateTime': start_time, 
            },
            'end': {
                'dateTime': end_time,   
            },
            'attendees': [
                {'email': player_email},
            ],
            }
        
        if self.event_id:
            updated_event = service.events().update(calendarId='primary', eventId=self.event_id, body=event).execute()
            return updated_event
        else:
            event = service.events().insert(calendarId='primary', body=event).execute()
            return event
            

    def check_user_availability(self):
        if self.assigned_end_time > self.assigned_start_time:

            all_available_events_for_day =AvailableData.objects.filter(user__user=self.user.user,available_start_time__date=self.assigned_end_time.date())
            start_time_vs_end_time_for_day= dict(all_available_events_for_day.values_list('available_start_time','available_end_time'))

            available_records_wrt_start_time = all_available_events_for_day.filter(available_start_time__lte = self.assigned_start_time)

            start_time_vs_end_time_for_day_wrt_start_time =dict(available_records_wrt_start_time.values_list('available_start_time','available_end_time'))
            
            for end_time in start_time_vs_end_time_for_day_wrt_start_time.values():
                if self.assigned_end_time <= end_time:
                    return True
                else:
                    for start,end in start_time_vs_end_time_for_day.items():
                        if end_time == start and self.assigned_end_time <= end:
                            return True



        

        
        
        




    



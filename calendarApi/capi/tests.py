from __future__ import unicode_literals

from django.test import TestCase
import datetime
from django.utils import timezone
from faker import Faker
import random  
import unittest
import factory
from .models import AssignementData,Availabledata,UserData,Credential
from mock import Mock, patch


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserData
    userID= random.randrange(0,100,2)
    personal_email= factory.Faker('email')
    Username = factory.Faker('name')

class AvailabledataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Availabledata
    user=factory.SubFactory(UserFactory)
    available_start_time=timezone.now()-datetime.timedelta(hours=1)
    available_end_time=timezone.now()+datetime.timedelta(hours=3)

class AssignementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignementData
    user=factory.SubFactory(UserFactory)
    assigned_start_time=timezone.now()
    assigned_end_time=timezone.now()+datetime.timedelta(hours=3)

class CredentialsDBFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Credential
    token="ya29.GltPB_fBqmTiFQZYvht1OfBZVjiTGeou7IJqfeEhnnYxClIOOdng3CYWDMgLUFyLt9vy49ltdo9gcfp3TagXO0Ofamky9dDyAqRP9YYj5VaZ9W38dgH6BOgwB68Y",
    refresh_token="1/wfAVNa-4VmsnZN8ct46eGCi2Hd4b1dm3ZseUvCMad34",
    user_email="gaurav.chaturvedi@squadrun.co",
    client_secret_file='{"web": {"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "redirect_uris": ["http://localhost:80", "http://87e9880f.ngrok.io/capi/capture_token"], "token_uri": "https://oauth2.googleapis.com/token", "javascript_origins": ["http://localhost:8080", "http://localhost:8000"], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "1011984601039-2aqu7si3gikf2h432rol61p6vn6chb5t.apps.googleusercontent.com", "client_secret": "CMokexzjmSigrMLvoj9LQgbR", "project_id": "calenderapi-246115"}}'
    

class Assignementdata_test(TestCase):

    def test_check_user_availability(self):
        user=AvailabledataFactory().user
        time_start= timezone.now()
        time_end = timezone.now() + datetime.timedelta(hours=1)
        check_availability = AssignementData(user=user,assigned_start_time=time_start,assigned_end_time=time_end)
        self.assertIs(check_availability.check_user_availability(), True)

    @patch('capi.models.AssignementData.insert_api_call')
    def test_save_calendar_event(self,mock_insert_api_call):
        new_task=AssignementFactory()
        mock_insert_api_call.return_value={"id":"vpadtdvcr0n9nreq95a293bkog"}
        new_task.save_calendar_event()
        self.assertIs(new_task.event_id,"vpadtdvcr0n9nreq95a293bkog")

class Availabledata_test(TestCase):

    def test_return_user_by_email(self):
        
        user=UserData.objects.create(userID= 1,personal_email="gauarv.chaturvedi@squadrun.co",
        Username = "Gaurav")
        userlist=UserData.objects.all()
        email="gauarv.chaturvedi@squadrun.co"
        user=UserData.objects.get(personal_email="gauarv.chaturvedi@squadrun.co")
        self.assertIs((Availabledata.return_userby_email(email,userlist)).userID,user.userID)

    
    
    def test_event_data(self):
        prev_count=Availabledata.objects.all().count()
        Credential.objects.create( token="ya29.GltPB_fBqmTiFQZYvht1OfBZVjiTGeou7IJqfeEhnnYxClIOOdng3CYWDMgLUFyLt9vy49ltdo9gcfp3TagXO0Ofamky9dDyAqRP9YYj5VaZ9W38dgH6BOgwB68Y",
        refresh_token="1/wfAVNa-4VmsnZN8ct46eGCi2Hd4b1dm3ZseUvCMad34",
        user_email="gaurav.chaturvedi@squadrun.co",
        client_secret_file={"web": {"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "redirect_uris": ["http://localhost:80", "http://87e9880f.ngrok.io/capi/capture_token"], "token_uri": "https://oauth2.googleapis.com/token", "javascript_origins": ["http://localhost:8080", "http://localhost:8000"], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "1011984601039-2aqu7si3gikf2h432rol61p6vn6chb5t.apps.googleusercontent.com", "client_secret": "CMokexzjmSigrMLvoj9LQgbR", "project_id": "calenderapi-246115"}}
        )
        time_start= timezone.now()+ datetime.timedelta(hours=4)
        time_end = timezone.now() + datetime.timedelta(hours=5)
        user=UserData.objects.create(userID= 2,personal_email="gauarv.chaturvedi@squadrun.co",
            Username = "Gaurav")
        Availabledata.objects.create(user=user,available_start_time=time_start,available_end_time=time_end)
            
        Availabledata.event_data("gaurav.chaturvedi@squadrun.co")
        next_count=Availabledata.objects.all().count()
        self.assertIs(next_count>prev_count,True)


class CredentialDB_test(TestCase):


    def test_return_url(self):
        Credential.objects.create(
        user_email="test@squadrun.co",
        client_secret_file={"web": {"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "redirect_uris": ["http://localhost:80", "http://87e9880f.ngrok.io/capi/capture_token"], "token_uri": "https://oauth2.googleapis.com/token", "javascript_origins": ["http://localhost:8080", "http://localhost:8000"], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "1011984601039-2aqu7si3gikf2h432rol61p6vn6chb5t.apps.googleusercontent.com", "client_secret": "CMokexzjmSigrMLvoj9LQgbR", "project_id": "calenderapi-246115"}}
        )
        test=Credential.return_url(email="test@squadrun.co")
        test_url=test.encode('ascii','ignore')
        self.assertIs(len(test_url) >100,True)

    @patch('google_auth_oauthlib.flow.Flow.fetch_token')
    def test_save_new_credential(self,mock_fetch_token):
        Credential.objects.create(
        user_email="test@squadrun.co",
        client_secret_file={"web": {"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "redirect_uris": ["http://localhost:80", "http://87e9880f.ngrok.io/capi/capture_token"], "token_uri": "https://oauth2.googleapis.com/token", "javascript_origins": ["http://localhost:8080", "http://localhost:8000"], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "1011984601039-2aqu7si3gikf2h432rol61p6vn6chb5t.apps.googleusercontent.com", "client_secret": "CMokexzjmSigrMLvoj9LQgbR", "project_id": "calenderapi-246115"}}
        )
        mock_fetch_token.return_value={
            "access_token":"jkdhfjkdsf",
            "refresh_token":"SDFFDGDfgdjkfngmdfngdSDs"
        }
        Credential.save_new_credential(code="code",email="test@squadrun.co")
        test=Credential.objects.get(user_email="test@squadrun.co")
        self.assertEqual(test.token,"jkdhfjkdsf")








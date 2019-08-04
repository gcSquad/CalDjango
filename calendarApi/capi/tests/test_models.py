from __future__ import unicode_literals

from django.test import TestCase
import datetime
import pytz
from django.utils import timezone 
from capi.models import AssignementData,AvailableData,UserData,Credential
from mock import Mock, patch
from capi.utils import return_dates_in_isoformat
from factories import UserFactory,AssignementFactory,AvailabledataFactory,CredentialFactory

class Assignementdata_test(TestCase):

    def test_check_user_availability(self):
        
        user=UserFactory(personal_email="gauarv.chaturvedi@squadrun.co",
            username = "SquadG",timeZone = pytz.timezone('Asia/Kolkata'))
        
        time_start= (timezone.now()- datetime.timedelta(hours=3)).astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now() + datetime.timedelta(hours=5)).astimezone(pytz.timezone('Asia/Kolkata'))
        AvailabledataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        
        assign_start=(timezone.now()).astimezone(pytz.timezone('Asia/Kolkata'))
        assign_end=(timezone.now() + datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        new_task=AssignementFactory(user=user,assigned_start_time=assign_start,assigned_end_time=assign_end)
        
        self.assertIs(new_task.check_user_availability(), True)

    @patch('capi.models.AssignementData.create_appointment_event')
    def test_save_appointment_to_calendar(self,mock_create_appointment_event):
        new_task=AssignementFactory()
        mock_create_appointment_event.return_value={"id":"vpadtdvcr0n9nreq95a293bkog"}
        new_task.save_appointment_to_calendar("gaurav.chaturvedi@squadrun.co")
        self.assertIs(new_task.event_id,"vpadtdvcr0n9nreq95a293bkog")

class Availabledata_test(TestCase):
      
    def test_save_new_events_in_db(self):
        prev_count=AvailableData.objects.all().count()
        
        CredentialFactory( token="ya29.GltPB_fBqmTiFQZYvht1OfBZVjiTGeou7IJqfeEhnnYxClIOOdng3CYWDMgLUFyLt9vy49ltdo9gcfp3TagXO0Ofamky9dDyAqRP9YYj5VaZ9W38dgH6BOgwB68Y",
        refresh_token="1/wfAVNa-4VmsnZN8ct46eGCi2Hd4b1dm3ZseUvCMad34",
        user_email="gaurav.chaturvedi@squadrun.co",
        client_secret_file={"web": {"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "redirect_uris": ["http://localhost:80", "http://87e9880f.ngrok.io/capi/capture_token"], "token_uri": "https://oauth2.googleapis.com/token", "javascript_origins": ["http://localhost:8080", "http://localhost:8000"], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "1011984601039-2aqu7si3gikf2h432rol61p6vn6chb5t.apps.googleusercontent.com", "client_secret": "CMokexzjmSigrMLvoj9LQgbR", "project_id": "calenderapi-246115"}}
        )

        time_start= timezone.now()+ datetime.timedelta(hours=3)
        time_end = timezone.now() + datetime.timedelta(hours=5)
        user=UserFactory(personal_email="gauarv.chaturvedi@squadrun.co",
            username = "Gaurav")
        AvailabledataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        
        event=[{
            "id":"sddsfbsdfm",
            "end":{
                "dateTime":return_dates_in_isoformat(5,'add')
            },
            "start":{
                "dateTime":return_dates_in_isoformat(4,'subtract')
            },
            "creator":{
                "email":"gaurav.chaturvedi@squadrun.co"
            }
        }] 

        new_test_object=  AvailableData.objects.get(user__username="Gaurav")
        new_test_object.save_new_events_in_db(event)
        next_count=AvailableData.objects.all().count()
        
        self.assertIs(next_count>prev_count,True)


class CredentialDB_test(TestCase):

    def test_return_auth_url(self):
        CredentialFactory(
        user_email="test@squadrun.co",
        client_secret_file={"web": {"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "redirect_uris": ["http://localhost:80", "http://87e9880f.ngrok.io/capi/capture_token"], "token_uri": "https://oauth2.googleapis.com/token", "javascript_origins": ["http://localhost:8080", "http://localhost:8000"], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "1011984601039-2aqu7si3gikf2h432rol61p6vn6chb5t.apps.googleusercontent.com", "client_secret": "CMokexzjmSigrMLvoj9LQgbR", "project_id": "calenderapi-246115"}}
        )
        credential_obj=Credential.objects.get(user_email="test@squadrun.co")

        test=credential_obj.return_auth_url()
        test_url=test.encode('ascii','ignore')
        self.assertIs(len(test_url) >100,True)

    @patch('google_auth_oauthlib.flow.Flow.fetch_token')
    def test_save_captured_token(self,mock_fetch_token):
        CredentialFactory(
        user_email="test@squadrun.co",
        state="abcdefgh",
        client_secret_file={"web": {"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "redirect_uris": ["http://localhost:80", "http://87e9880f.ngrok.io/capi/capture_token"], "token_uri": "https://oauth2.googleapis.com/token", "javascript_origins": ["http://localhost:8080", "http://localhost:8000"], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "1011984601039-2aqu7si3gikf2h432rol61p6vn6chb5t.apps.googleusercontent.com", "client_secret": "CMokexzjmSigrMLvoj9LQgbR", "project_id": "calenderapi-246115"}}
        )
        mock_fetch_token.return_value={
            "access_token":"jkdhfjkdsf",
            "refresh_token":"SDFFDGDfgdjkfngmdfngdSDs"
        }
        Credential.save_captured_token(code="code",email="test@squadrun.co",state="abcdefgh")
        test_credential_object=Credential.objects.get(user_email="test@squadrun.co")
        self.assertEqual(test_credential_object.token,"jkdhfjkdsf")











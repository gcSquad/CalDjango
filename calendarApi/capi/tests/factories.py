import datetime
import factory
from faker import Faker
from capi.models import AssignementData,AvailableData,UserData,Credential
import random 
import pytz
from django.utils import timezone

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserData
    personal_email= "gaurav.chaturvedi@squadrun.co"
    username = "SquadG"
    timeZone = pytz.timezone('Asia/Kolkata')

class AvailabledataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AvailableData
    user=factory.SubFactory(UserFactory)
    available_start_time=timezone.now()-datetime.timedelta(hours=3)
    available_end_time=timezone.now()+datetime.timedelta(hours=5)

class AssignementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignementData
    user=factory.SubFactory(UserFactory)
    assigned_start_time=timezone.now()
    assigned_end_time=timezone.now()+datetime.timedelta(hours=2)

class CredentialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Credential
    token="ya29.GltPB_fBqmTiFQZYvht1OfBZVjiTGeou7IJqfeEhnnYxClIOOdng3CYWDMgLUFyLt9vy49ltdo9gcfp3TagXO0Ofamky9dDyAqRP9YYj5VaZ9W38dgH6BOgwB68Y",
    refresh_token="1/wfAVNa-4VmsnZN8ct46eGCi2Hd4b1dm3ZseUvCMad34",
    user_email="gaurav.chaturvedi@squadrun.co",
    client_secret_file={"web": {"auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "redirect_uris": ["http://localhost:80", "http://87e9880f.ngrok.io/capi/capture_token"], "token_uri": "https://oauth2.googleapis.com/token", "javascript_origins": ["http://localhost:8080", "http://localhost:8000"], "auth_uri": "https://accounts.google.com/o/oauth2/auth", "client_id": "1011984601039-2aqu7si3gikf2h432rol61p6vn6chb5t.apps.googleusercontent.com", "client_secret": "CMokexzjmSigrMLvoj9LQgbR", "project_id": "calenderapi-246115"}}
        
   

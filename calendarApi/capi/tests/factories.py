import datetime
import factory
from factory import Sequence
from faker import Faker
from capi.models import AssignementData,AvailableData,UserData,Credential
from django.contrib.auth.models import User
import random 
import pytz
from django.utils import timezone

class UserDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserData
    personal_email= "gaurav.chaturvedi@squadrun.co"
    username = "SquadG"
    timeZone = pytz.timezone('Asia/Kolkata')

class AvailableDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AvailableData
    user=factory.SubFactory(UserDataFactory)
    available_start_time=timezone.now()-datetime.timedelta(hours=3)
    available_end_time=timezone.now()+datetime.timedelta(hours=5)

class AssignementDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignementData
    user=factory.SubFactory(UserDataFactory)
    assigned_start_time=timezone.now()
    assigned_end_time=timezone.now()+datetime.timedelta(hours=2)

class CredentialFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Credential
    token="dfngkdnfg",
    refresh_token="kjdvjkxcjv",
    user_email="gaurav.chaturvedi@squadrun.co",
    client_secret_file={"web": {}}

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda n: "user_{0}".format(n))
    password = "admin123"
   

   

from __future__ import unicode_literals

from django.test import TestCase
import datetime
from django.utils import timezone
from faker import Faker
import random  
import factory
from .models import Assignementdata,Availabledata,Userdata
from views import not_check_existing_event
import sys

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Userdata
    userID= random.randrange(0,100,2)
    personal_email= factory.Faker('email')
    Username = factory.Faker('name')

class AvailabledataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Availabledata
    userID=factory.SubFactory(UserFactory)
    available_start_time=timezone.now()-datetime.timedelta(hours=1)
    available_end_time=timezone.now()+datetime.timedelta(hours=3)

    

class Assignementdata_test(TestCase):

    def test_validate_entered_time(self):
        user=UserFactory()
        time_start= timezone.now()
        time_end = timezone.now() + datetime.timedelta(days=1)
        checktime = Assignementdata(userID=user,assigned_start_time=time_start,assigned_end_time=time_end)
        self.assertIs(checktime.validate_entered_time(), True)

    

    def test_check_user_availability(self):
        user=AvailabledataFactory().userID
        time_start= timezone.now()
        time_end = timezone.now() + datetime.timedelta(hours=1)
        check_availability = Assignementdata(userID=user,assigned_start_time=time_start,assigned_end_time=time_end)
        #print(check_availability.userID.userID,check_availability.userID.Username,check_availability.userID.personal_email)
        #sys.stderr.write(repr(check_availability) + '\n')
        self.assertIs(check_availability.check_user_availability(), True or None)

class Availabledata_test(TestCase):

    def test_not_check_existing_event(self):
        self.assertIs(not_check_existing_event("486ihp9uorri21r58u61t6l6nc"),True)


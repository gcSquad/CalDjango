from __future__ import unicode_literals

from django.test import TestCase
import datetime
from django.utils import timezone
from faker import Faker
import random  
import factory
from .models import Assignementdata,Availabledata,Userdata
from views import non_existing_event
# from unittest.mock import Mock, patch


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
        self.assertIs(check_availability.check_user_availability(), True)

    # @patch(Assignementdata.save_calendar_event)
    # def test_save_calendar_event(mock_get):
        


class Availabledata_test(TestCase):

    def test_non_existing_event(self):
        self.assertIs(non_existing_event("486ihp9uorri21r58u61t6l6nc"),True)


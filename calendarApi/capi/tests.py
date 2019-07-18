from __future__ import unicode_literals

from django.test import TestCase
import datetime
from django.utils import timezone
from faker import Faker
import random  
import unittest
import factory
from .models import Assignementdata,Availabledata,Userdata
from views import non_existing_event
from mock import Mock, patch


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

class AssignementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Assignementdata
    userID=factory.SubFactory(UserFactory)
    assigned_start_time=timezone.now()
    assigned_end_time=timezone.now()+datetime.timedelta(hours=3)

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

    # @patch(Assignementdata.insert_api_call)
    # def test_save_calendar_event(self,mock_insert_api_call):
    #     new_task=AssignementFactory()
    #     mock_insert_api_call.return_value='{"id":"vpadtdvcr0n9nreq95a293bkog"}'
    #     new_task.save_calendar_event()
    #     mock_insert_api_call.assert_called()

class Availabledata_test(TestCase):

    def test_non_existing_event(self):
        self.assertIs(non_existing_event("486ihp9uorri21r58u61t6l6nc"),True)


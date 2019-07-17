# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import datetime
from django.utils import timezone
from faker import Faker
import random  
# Create your tests here.
import factory
from .models import Assignementdata,Availabledata,Userdata

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Userdata
    userID= 99
    personal_email= factory.Faker('email')
    Username = factory.Faker('name')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Availabledata
    userID=UserFactory()
    available_start_time=timezone.now()-datetime.timedelta(hours=1)
    available_end_time=timezone.now()+datetime.timedelta(hours=3)

    

class Assignementdata_test(TestCase):

    def test_validate_entered_time(self):
        user=UserFactory()
        time_start= timezone.now()
        time_end = timezone.now() + datetime.timedelta(days=1)
        checktime = Assignementdata(userID=user,assigned_start_time=time_start,assigned_end_time=time_end)
        self.assertIs(checktime.validate_entered_time(), True)

    

    def test_check_user_availability():
        user=UserFactory()
        time_start= timezone.now()
        time_end = timezone.now() + datetime.timedelta(hours=1)
        checktime = Assignementdata(userID=user,assigned_start_time=time_start,assigned_end_time=time_end)
        self.assertIs(checktime.check_user_availability(), True)
        

# class Availabledata_test(TestCase):

    



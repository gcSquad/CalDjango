import datetime
import factory
from faker import Faker
import random 

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserData
    personal_email= factory.Faker('email')
    username = factory.Faker('name')
    timeZone = pytz.timezone('Asia/Kolkata')

class AvailabledataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AvailableData
    user=factory.SubFactory(UserFactory)
    available_start_time=timezone.now()-datetime.timedelta(hours=1)
    available_end_time=timezone.now()+datetime.timedelta(hours=3)

class AssignementFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AssignementData
    user=factory.SubFactory(UserFactory)
    assigned_start_time=timezone.now()
    assigned_end_time=timezone.now()+datetime.timedelta(hours=3)
   

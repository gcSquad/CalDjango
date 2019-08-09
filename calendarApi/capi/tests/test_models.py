from __future__ import unicode_literals

from django.test import TestCase
import datetime
import pytz
from django.utils import timezone 
from capi.models import AssignementData,AvailableData,UserData,Credential
from mock import Mock,patch,MagicMock
from capi.utils import return_dates_in_isoformat
from django.core.exceptions import ValidationError
from factories import UserDataFactory,AssignementDataFactory,AvailableDataFactory,CredentialFactory

class AssignementDataTestCase(TestCase):

    @patch('capi.models.AssignementData.check_user_availability')
    def test_clean(self,mock_check_user_availability):
        user=UserDataFactory(personal_email="gauarv.chatkdfhg@un.co",
            username = "SquadG",timeZone = pytz.timezone('Asia/Kolkata'))
        time_start= timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()- datetime.timedelta(hours=5)).astimezone(pytz.timezone('Asia/Kolkata'))
        test_object=AssignementDataFactory(user=user,assigned_start_time=time_start,assigned_end_time=time_end)
        with self.assertRaisesMessage(ValidationError, "End time Can't be less than start time for assignement!!"):
            test_object.clean()
        
        time_start= timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()+datetime.timedelta(hours=5)).astimezone(pytz.timezone('Asia/Kolkata'))
        test_object=AssignementDataFactory(user=user,assigned_start_time=time_start,assigned_end_time=time_end)
        mock_check_user_availability.return_value=False
        with self.assertRaisesMessage(ValidationError, "Selected User is not available for given time slot!!"):
            test_object.clean()



    def test_check_user_availability(self):
        
        user=UserDataFactory(personal_email="gauarv.chaturvedi@squadrun.co",
            username = "SquadG",timeZone = pytz.timezone('Asia/Kolkata'))
        
        time_start= (timezone.now()- datetime.timedelta(hours=3)).astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now() + datetime.timedelta(hours=5)).astimezone(pytz.timezone('Asia/Kolkata'))
        AvailableDataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        assign_start=(timezone.now()).astimezone(pytz.timezone('Asia/Kolkata'))
        assign_end=(timezone.now() + datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        new_task=AssignementDataFactory(user=user,assigned_start_time=assign_start,assigned_end_time=assign_end)
        with self.assertNumQueries(3): #thought 2????
            self.assertIs(new_task.check_user_availability(), True)


        time_start= (timezone.now()- datetime.timedelta(hours=3)).astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()- datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        AvailableDataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        time_start= (timezone.now()- datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()+ datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        AvailableDataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        assign_start=(timezone.now()- datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        assign_end=(timezone.now() + datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        new_task=AssignementDataFactory(user=user,assigned_start_time=assign_start,assigned_end_time=assign_end)
        with self.assertNumQueries(3):
            self.assertIs(new_task.check_user_availability(), True)

        
        time_start= (timezone.now()- datetime.timedelta(hours=3)).astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()+ datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        AvailableDataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        time_start= (timezone.now()- datetime.timedelta(hours=1)).astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()).astimezone(pytz.timezone('Asia/Kolkata'))
        AvailableDataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        assign_start=(timezone.now()- datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        assign_end=(timezone.now()).astimezone(pytz.timezone('Asia/Kolkata'))
        new_task=AssignementDataFactory(user=user,assigned_start_time=assign_start,assigned_end_time=assign_end)
        with self.assertNumQueries(3):
            self.assertIs(new_task.check_user_availability(), True)

        time_start= (timezone.now()- datetime.timedelta(hours=3)).astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()).astimezone(pytz.timezone('Asia/Kolkata'))
        AvailableDataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        time_start= (timezone.now()).astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()+ datetime.timedelta(hours=3)).astimezone(pytz.timezone('Asia/Kolkata'))
        AvailableDataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        assign_start=(timezone.now()- datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        assign_end=(timezone.now()+ datetime.timedelta(hours=2)).astimezone(pytz.timezone('Asia/Kolkata'))
        new_task=AssignementDataFactory(user=user,assigned_start_time=assign_start,assigned_end_time=assign_end)
        with self.assertNumQueries(3):
            self.assertIs(new_task.check_user_availability(), True)



    @patch('capi.models.AssignementData.create_appointment_event')
    def test_save_appointment_to_calendar(self,mock_create_appointment_event):
        new_task=AssignementDataFactory()
        mock_create_appointment_event.return_value={"id":"vpadtdvcr0n9nreq95a293bkog"}
        with self.assertNumQueries(1): 
            new_task.save_appointment_to_calendar("gaurav.chaturvedi@squadrun.co")
        self.assertIs(new_task.event_id,"vpadtdvcr0n9nreq95a293bkog")



class AvailableDataTestCase(TestCase):
      
    def test_save_new_events_in_db(self):
        prev_count=AvailableData.objects.all().count()
        
        CredentialFactory( token="kcvhxcklvxvvcklxc",
        refresh_token="cxnv,mxncvmnxcnxm",
        user_email="gaurav.chaturvedi@squadrun.co",
        client_secret_file={"web": {}}
        )

        time_start= timezone.now()+ datetime.timedelta(hours=3)
        time_end = timezone.now() + datetime.timedelta(hours=5)
        user=UserDataFactory(personal_email="gauarv.chaturvedi@squadrun.co",
            username = "Gaurav")
        AvailableDataFactory(user=user,available_start_time=time_start,available_end_time=time_end)
        
        new_event=[{
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

        random_event=[{
            "id":"sjjbjckbx",
            "end":{
                "dateTime":return_dates_in_isoformat(5,'add')
            },
            "start":{
                "dateTime":return_dates_in_isoformat(4,'subtract')
            },
            "creator":{
                "email":"gfhvjkxchv@ncv.co"
            }
        }] 

        new_test_object = AvailableData.objects.get(user__username="Gaurav")
        with self.assertNumQueries(2):#thought 3..ask????
            new_test_object.save_new_events_in_db(new_event)
        next_count=AvailableData.objects.all().count() 
        self.assertIs(next_count==prev_count+1,True)

        new_object = AvailableData.objects.get(user__username="Gaurav")
        with self.assertNumQueries(2):
            new_object.save_new_events_in_db(new_event)
        new_count=AvailableData.objects.all().count() 
        self.assertIs(next_count==new_count,True)

        fail_object = AvailableData.objects.get(user__username="Gaurav")
        with self.assertNumQueries(2):
            fail_object.save_new_events_in_db(random_event)
        fail_count=AvailableData.objects.all().count() 
        self.assertIs(next_count==fail_count,True)




class CredentialTestCase(TestCase):

    @patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_config')
    def test_return_auth_url(self,mock_from_client_config):
        CredentialFactory(
        user_email="test@squadrun.co",
        client_secret_file={"web": {}}
        )
        mock_flow=MagicMock()
        mock_flow.redirect_uri="anything"
        credential_obj=Credential.objects.get(user_email="test@squadrun.co")
        mock_from_client_config.return_value=mock_flow
        mock_flow.authorization_url.return_value='test_url','test_state'
        with self.assertNumQueries(1):
            test=credential_obj.return_auth_url()
        self.assertIs(test,"test_url")


    @patch('google_auth_oauthlib.flow.InstalledAppFlow.from_client_config')
    def test_save_captured_token(self,mock_from_client_config):
        CredentialFactory(
        user_email="test@squadrun.co",
        state="abcdefgh",
        client_secret_file={"web": {}}
        )
        mock_flow=MagicMock()
        mock_flow.redirect_uri="anything"
        mock_from_client_config.return_value=mock_flow
        mock_flow.fetch_token.return_value={
            "access_token":"jkdhfjkdsf",
            "refresh_token":"SDFFDGDfgdjkfngmdfngdSDs"
        }
        with self.assertNumQueries(2):
            Credential.save_captured_token(code="code",email="test@squadrun.co",state="abcdefgh")
        test_credential_object=Credential.objects.get(user_email="test@squadrun.co")
        self.assertEqual(test_credential_object.token,"jkdhfjkdsf")
        self.assertEqual(test_credential_object.refresh_token,"SDFFDGDfgdjkfngmdfngdSDs")

    












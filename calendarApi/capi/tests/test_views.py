from django.test import TestCase
from rest_framework.test import APITestCase
from capi.models import AssignementData,AvailableData,UserData,Credential
from factories import UserDataFactory,AssignementDataFactory,AvailableDataFactory,CredentialFactory,UserFactory
from capi.views import capture_token,import_data
from django.contrib.auth.models import User
from django.test import Client
from mock import Mock, patch
from django.urls import reverse
from rest_framework import status
import pytz
import datetime
from django.utils import timezone 

class LoginViewTestCase(APITestCase):

    def test_get_without_login(self):
        response = self.client.get('/capi/login/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_get_with_login(self):
        User.objects.create_user('gaurav', password='admin123')
        self.client.login(username='gaurav', password='admin123')
        response = self.client.get('/capi/login/', follow=True)
        self.assertRedirects(response,'/capi/',302)

    def test_post_with_credentials(self):
        User.objects.create_user('gaurav', password='admin123')
        url='/capi/login/'
        data={
            "username":"gaurav",
            "password":"admin123"
        }
        response = self.client.post(url,data)
        self.assertRedirects(response,'/capi/',302)
        
    def test_post_without_credentials(self):
        User.objects.create_user('kjdbfvj', password='nxcbv')
        url='/capi/login/'
        data={
            "username":"xmcbv",
            "password":"skjdgv"
        }
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertEquals(response.context['invalid_user'], True)
        

class TestHomeViewCase(TestCase):

    def test_call_view_home(self):
        User.objects.create_user('SquadG', password='admin123')
        user=UserDataFactory(personal_email="gauarv.chatkdfhg@un.co",
            username = "SquadG",timeZone = pytz.timezone('Asia/Kolkata'))
        time_start= timezone.now().astimezone(pytz.timezone('Asia/Kolkata'))
        time_end = (timezone.now()- datetime.timedelta(hours=5)).astimezone(pytz.timezone('Asia/Kolkata'))
        test_object=AssignementDataFactory(user=user,assigned_start_time=time_start,assigned_end_time=time_end)
        time_check=(time_start.astimezone(pytz.timezone('Asia/Kolkata'))).strftime("%d %b, %Y %I:%M %p")
        self.client.login(username="SquadG", password='admin123')
        with self.assertNumQueries(4): #again missed one session and auth hit so thought 2 initially
            response = self.client.get('/capi/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertEquals(response.context['assignment_records'][0].assigned_start_time,time_check)



class CaptureTokenTestCase(TestCase):
    @patch('capi.models.Credential.save_captured_token')
    def test_capture_token(self,mock_save_captured_token):

        self.user = User.objects.create_user(username='gaurav', password='admin123',email="test@squadrun.co")
        self.client.login(username='gaurav', password='admin123')
        
        with self.assertNumQueries(2): #thought 1
            response = self.client.get('/capi/capture-token/',{'state':"sdncsnd",'code':"cjskdcss"})
        
        mock_save_captured_token.assert_called_with(code=u'cjskdcss', email=u'test@squadrun.co', state=u'sdncsnd')

        with self.assertNumQueries(2): #thought 0
            response = self.client.get('/capi/capture-token/')
        self.assertEqual(response['Location'],'/admin/capi/availabledata/')
        self.assertEqual(response.status_code,302)
        

class ImportDataTestCase(TestCase):
    @patch('capi.models.Credential.get_fresh_available_data')
    @patch('capi.models.AvailableData.save_new_events_in_db')
    @patch('capi.models.Credential.return_auth_url')
    def test_import_data(self,mock_return_auth_url,mock_save_new_events_in_db,mock_get_fresh_available_data):

        self.user = User.objects.create_user(username='gaurav', password='admin123',email="test@squadrun.co")
        self.client.login(username='gaurav', password='admin123')
        
        UserDataFactory(username='gaurav',personal_email='test@squadrun.co')
        credential=CredentialFactory(token="qwerty",refresh_token="abcd",user_email="test@squadrun.co",
        client_secret_file='{"key:Value"}')
        with self.assertNumQueries(3):
            response = self.client.get('/capi/available-data/')

        mock_get_fresh_available_data.__str__.return_value="anything"
        mock_save_new_events_in_db.assert_called_with(mock_get_fresh_available_data.return_value)
        
        credential=CredentialFactory(user_email="test2@squadrun.co",client_secret_file='{"key:Value"}')
        with self.assertNumQueries(3): #ask Nitish should have been 1
            response = self.client.get('/capi/available-data/')
        self.assertEqual(response['Location'],'/admin/capi/availabledata/')
        self.assertEqual(response.status_code,302)
        
        # self.user = User.objects.create_user(username='test', password='admin123',email="testing@squadrun.co")
        # credential=CredentialFactory(user_email="testing@squadrun.co",client_secret_file='{"key:Value"}')
        # response = self.client.get('/capi/available-data/')
        # mock_return_auth_url.return_value="return-url"
        # print(response)
        
        
        



       



        
 





    





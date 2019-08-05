from django.test import TestCase
from capi.models import AssignementData,AvailableData,UserData,Credential
from factories import UserFactory,AssignementFactory,AvailabledataFactory,CredentialFactory
from capi.views import capture_token,import_data
from django.contrib.auth.models import User
from django.test import Client
from mock import Mock, patch

class TestViews(TestCase):

    def test_call_view_home(self):
        self.client.login(username='gaurav', password='admin123') 
        response = self.client.get('/capi/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_call_view_login_get(self):
        response = self.client.get('/capi/login/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

class CaptureTokenTest(TestCase):
    @patch('capi.models.Credential.save_captured_token')
    def test_capture_token(self,mock_save_captured_token):

        self.user = User.objects.create_user(username='gaurav', password='admin123',email="test@squadrun.co")
        self.client.login(username='gaurav', password='admin123')
        
        response = self.client.get('/capi/capture-token/',{'state':"sdncsnd",'code':"cjskdcss"})
        
        mock_save_captured_token.assert_called_with(code=u'cjskdcss', email=u'test@squadrun.co', state=u'sdncsnd')

class ImportDataTest(TestCase):
    @patch('capi.models.Credential.get_fresh_available_data')
    @patch('capi.models.AvailableData.save_new_events_in_db')
    def test_import_data(self,mock_save_new_events_in_db,mock_get_fresh_available_data):

        self.user = User.objects.create_user(username='gaurav', password='admin123',email="test@squadrun.co")
        self.client.login(username='gaurav', password='admin123')
        
        UserFactory(username='gaurav',personal_email='test@squadrun.co')
        credential=CredentialFactory(token="qwerty",refresh_token="abcd",user_email="test@squadrun.co",
        client_secret_file='{"key:Value"}')
        
        response = self.client.get('/capi/available-data/')

        mock_get_fresh_available_data.__str__.return_value="anything"
        mock_save_new_events_in_db.assert_called_with(mock_get_fresh_available_data.return_value)

       



        
 





    





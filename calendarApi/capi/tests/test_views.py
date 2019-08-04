from django.test import TestCase
from capi.models import AssignementData,AvailableData,UserData,Credential
from factories import UserFactory,AssignementFactory,AvailabledataFactory
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

# class CaptureTokenTest(TestCase):
#     @patch('capi.models.Credential.save_captured_token')
#     def test_capture_token(self,mock_save_captured_token):
#         UserFactory(personal_email="gauarv.chaturvedi@squadrun.co",
#             username = "gaurav")
#         #self.client.login(username='gaurav', password='admin123')
#         #c = Client()
#         response = self.client.get('/capi/capture-token/',{'state':"sdncsnd",'code':"cjskdcss",'user.email':"test@squadrun.co"})
#         mock_save_captured_token.return_value=None
#         mock_save_captured_token.assert_called()




    





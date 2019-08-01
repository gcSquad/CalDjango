from django.test import RequestFactory, TestCase
from django.utils import timezone 
from capi.models import AssignementData,AvailableData,UserData,Credential
from factories import UserFactory,AssignementFactory,AvailabledataFactory
from capi.views import capture_token,import_data
from django.contrib.auth.models import AnonymousUser, User

class CaptureTokenTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()

    def test_capture_token(self):
        request = self.factory.get('/capi/capture-token/')
        request.state="sbdfnmbsd"
        request.code="jsbdjvsdsj"
        request.user.email = self.user.personal_email
        response = capture_token(request)
        self.assertEqual(response.status_code, 200)

class ImportDataTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = UserFactory()

    def test_capture_token(self):
        request = self.factory.get('/capi/available-data/')
        request.user.email = self.user.personal_email
        response = import_data(request)
        self.assertEqual(response.status_code, 200)

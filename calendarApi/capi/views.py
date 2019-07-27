from __future__ import print_function

from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse
from .models import AvailableData,UserData,AssignementData,Credential
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import userSerializer,assignedDataSerializer
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from requests.exceptions import ConnectionError
import json


def capture_token(request):
    try:
        state=request.GET["state"]
        code=request.GET["code"]
    except ConnectionError as error:
        messages.error(request,error)
        return HttpResponseRedirect(reverse('admin:capi_availabledata_changelist'))

    
    Credential.save_captured_token(state=state,code=code,email=request.user.email)
    return HttpResponseRedirect(reverse('import_data'))

def import_data(request):
    try:
        user_credentials = Credential.objects.get(user_email=request.user.email)
    except Credential.DoesNotExist:
        messages.error(request,'Please create a user with necessary credentials !!')
        return HttpResponseRedirect(reverse('admin:capi_availabledata_changelist'))

    if not user_credentials.token:
        auth_url_for_access_token=user_credentials.return_auth_url()
        return redirect(auth_url_for_access_token)

    events = user_credentials.get_fresh_available_data()
    AvailableData.save_new_events_in_db(events)
    return HttpResponseRedirect(reverse('admin:capi_availabledata_changelist'))


class GetUserList(APIView):
    def get(self, request):
        users = UserData.objects.all()
        serialized = userSerializer(users, many=True)
        return Response(serialized.data)

                
class GetAssignmentList(APIView):
    def get(self,request):
        assignment_objects=AssignementData.objects.all()
        serialized = assignedDataSerializer(assignment_objects, many=True)
        return Response(serialized.data)

class Login(APIView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self,request,format=None):
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
          else:
              messages.error(request,"wrong username/password")
              return Response(request,self.template_name)


def logout(request):
    return render(request,'logout.html')

def home(request):
    return render(request,'home.html')



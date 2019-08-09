from __future__ import print_function

from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse
from .models import AvailableData,UserData,AssignementData,Credential
from rest_framework.views import APIView
from django.views.generic import TemplateView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.views.generic import ListView
from rest_framework import status
from requests.exceptions import ConnectionError
import json
from django.contrib.auth.decorators import login_required

@login_required
def capture_token(request):
    try:
        state=request.GET["state"]
        code=request.GET["code"]
    except KeyError:
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


class Login(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('home'))
        return render(request, self.template_name)

    def post(self,request,format=None):

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            context={
                  "invalid_user":True
            }
            return render(request,'login.html',context)

def logout_user(request):
    logout(request)
    return render(request,'logout.html')

def render_home(request):
    assignment_records= AssignementData.objects.filter(user=request.user.id)
    user_timezone=UserData.objects.get(id=request.user.id).timeZone
    for assignment in assignment_records:
        assignment.assigned_start_time =(assignment.assigned_start_time.astimezone(user_timezone)).strftime("%d %b, %Y %I:%M %p")
        assignment.assigned_end_time =(assignment.assigned_end_time.astimezone(user_timezone)).strftime("%d %b, %Y %I:%M %p")    
    context={
                  "assignment_records":assignment_records
            }
    return render(request,'home.html',context)





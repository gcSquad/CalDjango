from __future__ import print_function

from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse
from .models import Availabledata,Userdata,Assignementdata,CredentialsDB
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import userSerializer,assignedDataSerializer
from django.views.decorators.csrf import csrf_exempt


def redirect_to_auth_url(email):
    url=CredentialsDB.return_url(email)
    return redirect(url)

def capture_token(request):
    state=request.GET["state"]
    code=request.GET["code"]
    CredentialsDB.save_new_credential(state=state,code=code,email=request.user.email)
    return redirect('/admin/capi/availabledata')

def capture_token(request):
    state=request.GET["state"]
    code=request.GET["code"]
    CredentialsDB.save_new_credential(state=state,code=code,email=request.user.email)
    return redirect('/admin/capi/availabledata')

def import_data(request):
    try:
        user_exist= CredentialsDB.objects.get(user_email=request.user.email)
    except CredentialsDB.DoesNotExist:
        print("Please create User !!!!")
        return redirect('/admin/capi/availabledata')
    if not user_exist.token:
        return redirect_to_auth_url(request.user.email)

    Availabledata.event_data(request.user.email)  
    return redirect('/admin/capi/availabledata')   
        # return HttpResponseRedirect(reverse('import_data'))

class Get_user_List(APIView):
    def get(self, request):
        users = Userdata.objects.all()
        serialized = userSerializer(users, many=True)
        return Response(serialized.data)

                
class Get_assignment_List(APIView):
    def get(self,request):
        assignment=Assignementdata.objects.all()
        serialized = assignedDataSerializer(assignment, many=True)
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
            return HttpResponseRedirect("/capi/")
          else:
              print ("wrong username/password")
              return Response(request,self.template_name)


def user_logout(request):
    return render(request,'logout.html')

def home(request):
    return render(request,'home.html')



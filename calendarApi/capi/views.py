from __future__ import print_function

from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse
from .models import Availabledata,Userdata,Assignementdata
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import userSerializer,assignedDataSerializer
from django.views.decorators.csrf import csrf_exempt

def import_data(request):
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

def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user is not None:
            login(request, user)
            return HttpResponseRedirect("/capi/")
          else:
              print ("wrong username/password")
              return render(request,'login.html')
    else:
        return render(request,'login.html')

def user_logout(request):
    return render(request,'logout.html')

def home(request):
    return render(request,'home.html')

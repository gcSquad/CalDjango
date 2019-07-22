from __future__ import print_function

# from django.http import HttpResponseRedirect
from django.shortcuts import redirect,render
from django.urls import reverse
from .models import Availabledata,Userdata,Assignementdata
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import userSerializer,assignedDataSerializer

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

    

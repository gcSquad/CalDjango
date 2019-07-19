from __future__ import print_function
from django.shortcuts import redirect
from django.shortcuts import render
from .models import Availabledata,Userdata,Assignementdata
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import userSerializer,assignedDataSerializer

def import_data(request):
    Availabledata.event_data()        
    return redirect("{% url 'import_data' %}")

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

    

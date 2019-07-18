from __future__ import print_function
import datetime   
import pickle
from googleapiclient.discovery import build
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Availabledata,Userdata

def import_data(request):
    Availabledata.get_event_data()        
    return redirect('/admin/capi/availabledata')


                

    

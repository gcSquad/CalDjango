from __future__ import print_function
from django.shortcuts import redirect
from .models import Availabledata,Userdata

def import_data(request):
    Availabledata.event_data()        
    return redirect('/admin/capi/availabledata')




                

    

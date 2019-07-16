from __future__ import absolute_import,print_function
from celery import shared_task

@shared_task 
def setappointment(record_id):
    print("jhvcjkbzxjkc")
    from capi.models import Assignementdata
    Assignementdata.objects.get(id=record_id).save_calendar_event()

   

    
        

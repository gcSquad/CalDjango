from __future__ import absolute_import,print_function
from celery import shared_task

@shared_task 
def setappointment(record_id):
    from capi.models import AssignementData
    AssignementData.objects.get(id=record_id).save_appointment()

   

    
        

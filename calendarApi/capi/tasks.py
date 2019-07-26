from __future__ import absolute_import,print_function
from celery import shared_task

@shared_task 
def set_calendar_appointment(record_id,current_user_email):
    from capi.models import AssignementData
    assignment_object=AssignementData.objects.get(id=record_id)
    if(assignment_object.event_id):
        assignment_object.update_appointment_in_calendar(current_user_email)
    else:
        assignment_object.save_appointment_to_calendar(current_user_email)

   

    
        

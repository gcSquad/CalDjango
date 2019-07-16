# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from capi.models import Userdata,Availabledata,Assignementdata

class UserdataAdmin(admin.ModelAdmin):
    list_display=('userID','Username','personal_email')
class AvailabledataAdmin(admin.ModelAdmin):
    list_display=('userID','available_start_time','available_end_time')
 #   actions = [refresh]

class AssignementAdmin(admin.ModelAdmin):
    list_display=('userID','assigned_start_time','assigned_end_time')
    exclude=('event_id',)
    

admin.site.register(Userdata,UserdataAdmin)
admin.site.register(Availabledata,AvailabledataAdmin)
admin.site.register(Assignementdata,AssignementAdmin)
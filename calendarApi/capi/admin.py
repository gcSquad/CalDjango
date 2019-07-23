# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from capi.models import Userdata,Availabledata,Assignementdata,CredentialsDB

class UserdataAdmin(admin.ModelAdmin):
    list_display=('userID','Username','personal_email')
class AvailabledataAdmin(admin.ModelAdmin):
    list_display=('userID','available_start_time','available_end_time')
 #   actions = [refresh]

class AssignementAdmin(admin.ModelAdmin):
    list_display=('userID','assigned_start_time','assigned_end_time')
    exclude=('event_id',)

class CredentialsAdmin(admin.ModelAdmin):
    list_display=('user_email','token','refresh_token','client_secret_file')   

admin.site.register(Userdata,UserdataAdmin)
admin.site.register(Availabledata,AvailabledataAdmin)
admin.site.register(Assignementdata,AssignementAdmin)
admin.site.register(CredentialsDB,CredentialsAdmin)
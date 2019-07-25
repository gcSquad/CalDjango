# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from capi.models import UserData,AvailableData,AssignementData,Credential

class UserdataAdmin(admin.ModelAdmin):
    list_display=('userID','Username','personal_email')
class AvailabledataAdmin(admin.ModelAdmin):
    list_display=('user','available_start_time','available_end_time')
 #   actions = [refresh]

class AssignementAdmin(admin.ModelAdmin):
    list_display=('user','assigned_start_time','assigned_end_time')
    exclude=('event_id',)

class CredentialsAdmin(admin.ModelAdmin):
    list_display=('user_email','state','token','refresh_token','client_secret_file')   

admin.site.register(UserData,UserdataAdmin)
admin.site.register(AvailableData,AvailabledataAdmin)
admin.site.register(AssignementData,AssignementAdmin)
admin.site.register(Credential,CredentialsAdmin)
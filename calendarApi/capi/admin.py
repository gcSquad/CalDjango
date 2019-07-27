# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tasks import set_calendar_appointment
from django.db import transaction
from django.contrib import admin
from capi.models import UserData,AvailableData,AssignementData,Credential

class UserDataAdmin(admin.ModelAdmin):
    list_display=('user','username','personal_email')

class AvailableDataAdmin(admin.ModelAdmin):
    list_display=('user','available_start_time','available_end_time')
    readonly_fields=('user','available_start_time','available_end_time','event_id',)

class AssignementAdmin(admin.ModelAdmin):
    list_display=('user','assigned_start_time','assigned_end_time','event_id')
    readonly_fields=('event_id',)

    def save_model(self, request, obj, form, change):
        super(AssignementAdmin, self).save_model(request, obj, form, change)
        transaction.on_commit(lambda:set_calendar_appointment.delay(obj.id,request.user.email))

class CredentialsAdmin(admin.ModelAdmin):
    list_display=('user_email','state','token','refresh_token','client_secret_file')
    readonly_fields = ('state','token','refresh_token',)   

admin.site.register(UserData,UserDataAdmin)
admin.site.register(AvailableData,AvailableDataAdmin)
admin.site.register(AssignementData,AssignementAdmin)
admin.site.register(Credential,CredentialsAdmin)
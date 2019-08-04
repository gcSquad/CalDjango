# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tasks import set_calendar_appointment
from django.db import transaction
from django.contrib import admin
from capi.models import UserData,AvailableData,AssignementData,Credential

class UserDataAdmin(admin.ModelAdmin):
    list_display=('username','personal_email','timeZone')
    
class AvailableDataAdmin(admin.ModelAdmin):
    change_list_template = 'admin/demo_change_list.html'
    list_display=('user','start_time','end_time')
    readonly_fields=('user','start_time','end_time','event_id',)

    def changelist_view(self, request, extra_context=None):
        return super(AvailableDataAdmin, self).changelist_view(request, extra_context=extra_context)

    def start_time(request,obj):
        user_timezone=obj.user.timeZone
        start_time =obj.available_start_time.astimezone(user_timezone)
        return start_time.strftime("%d %b, %Y %I:%M %p")
    
    def end_time(request,obj):
        user_timezone=obj.user.timeZone
        end_time =obj.available_end_time.astimezone(user_timezone)
        return end_time.strftime("%d %b, %Y %I:%M %p")
    

class AssignementAdmin(admin.ModelAdmin):
    list_display=('user','start_time','end_time','event_id')
    readonly_fields=('event_id',)

    def start_time(request,obj):
        user_timezone=obj.user.timeZone
        start_time =obj.assigned_start_time.astimezone(user_timezone)
        return start_time.strftime("%d %b, %Y %I:%M %p")
    
    def end_time(request,obj):
        user_timezone=obj.user.timeZone
        end_time =obj.assigned_end_time.astimezone(user_timezone)
        return end_time.strftime("%d %b, %Y %I:%M %p")

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
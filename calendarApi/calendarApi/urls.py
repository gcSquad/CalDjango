"""calendarApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.contrib import admin
from capi import views


urlpatterns = [
    url(r'^$', auth_views.login,{'template_name': 'home.html'}, name='home'),
    url(r'^login/$', auth_views.login,{'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,{'template_name': 'logged_out.html'}, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^capi/', include('capi.urls')),
    url(r'^userapi$', views.Get_user_List.as_view(),name='userapi'),
    url(r'^assignmentapi$', views.Get_assignment_List.as_view(),name='assignmentapi'),
    # url(r'^api-auth/', include('rest_framework.urls')),
    # url(r'^rest-auth/', include('rest_auth.urls')),
    #url(r'^capi/availabledata/new',),
    
]


from django.conf.urls import url, include
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView


from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^capture_token$',views.capture_token,name='capture_token'),
    url(r'^availabledata/',views.import_data, name='import_data'),
    url(r'^userapi$', views.Get_user_List.as_view(),name='userapi'),
    url(r'^assignmentapi$', views.Get_assignment_List.as_view(),name='assignmentapi'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^capture_token/$', views.capture_token, name='capturetoken'),
]

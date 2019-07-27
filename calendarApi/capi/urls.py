
from django.conf.urls import url, include
from django.http import HttpResponseRedirect
from django.views.generic.base import RedirectView


from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^capture-token/$',views.capture_token,name='capture_token'),
    url(r'^available-data/$',views.import_data, name='import_data'),
    url(r'^user-list-api/$', views.GetUserList.as_view(),name='user_list_api'),
    url(r'^assignment-api/$', views.GetAssignmentList.as_view(),name='assignment_api'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]


from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^availabledata/', views.import_data, name='import_data'),
    url(r'^userapi$', views.Get_user_List.as_view(),name='userapi'),
    url(r'^assignmentapi$', views.Get_assignment_List.as_view(),name='assignmentapi'),
]

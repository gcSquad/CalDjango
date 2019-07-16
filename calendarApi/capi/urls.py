
from django.conf.urls import url, include
from . import views
urlpatterns = [
    url(r'^availabledata/', views.import_data, name='import_data'),
]

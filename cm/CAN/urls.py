from django.urls import path

from CAN.views import *

urlpatterns = [
    path('show/', show, name='show'),
    path('can_search/', can_search, name='can_search'),
    path('analysis_data/', analysis_data, name='analysis_data'),
    path('test/', test, name='test'),
]
from django.urls import path

from video.views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('get_data/', get_data, name='get_data'),
]
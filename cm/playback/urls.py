from django.urls import path

from playback.views import *

urlpatterns = [
    path('back_video/', back_video, name='back_video'),
    path('search/', search, name='search'),
]
from django.urls import path

from lock.views import *

urlpatterns = [
    path('lock/', lock, name='lock'),
    path('llock/(?P<id>\d+)', llock, name='llock'),
    path('unlock/(?P<id>\d+)', unlock, name='unlock'),
]
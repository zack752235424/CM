from django.urls import path

from lock.views import *

urlpatterns = [
    path('lock/', lock, name='lock'),
    path('llock/(?P<VIN>\d+)', llock, name='llock'),
    path('unlock/(?P<VIN>\d+)', unlock, name='unlock'),
    path('check_status/(?P<VIN>\d+)', check_status, name='check_status'),
    path('search/', search, name='search'),
]
from django.urls import path

from lock.views import *

urlpatterns = [
    path('lock/', lock, name='lock'),
    path('llock/', llock, name='llock'),
    path('unlock/', unlock, name='unlock'),
    path('check_status/', check_status, name='check_status'),
    path('search/', search, name='search'),
    path('ledao_lock/', ledao_lock, name='ledao_lock'),
]
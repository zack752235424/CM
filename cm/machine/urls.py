from django.urls import path

from machine.views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('get_machine/', get_machine, name='get_machine'),
    path('machine_edit/', machine_edit, name='machine_edit'),
    path('machine_del/', machine_del, name='machine_del'),
    path('machine_add/', machine_add, name='machine_add'),
    path('machine_download', machine_download, name='machine_download'),
    path('machine_upload/', machine_upload, name='machine_upload'),
]
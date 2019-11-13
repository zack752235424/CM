from django.urls import path

from updt.views import *

urlpatterns = [
    path('up/', up, name='up'),
    path('get_users/', get_users, name='get_users'),
    path('up_download/', up_download, name='up_download'),
]
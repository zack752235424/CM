from django.urls import path

from updt.views import *

urlpatterns = [
    path('up/', up, name='up'),
    path('users/', users, name='users'),
]
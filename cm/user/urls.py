from django.urls import path

from user.views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('index/', index, name='index'),
]
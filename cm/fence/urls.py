from django.urls import path

from fence.views import *

urlpatterns = [
    path('index/', index, name='index'),
]
from django.urls import path

from index.views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('map/', map, name='map'),
    path('search/', search, name='search'),
]
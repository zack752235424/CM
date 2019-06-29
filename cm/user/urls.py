from django.urls import path

from user.views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout')
]
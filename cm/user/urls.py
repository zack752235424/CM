from django.urls import path

from user.views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('manage/', manage, name='manage'),
    path('member_add/', member_add, name='member_add'),
    path('edit/', edit, name='edit'),
    path('member_del/', member_del, name='member_del'),
    path('member_search/', member_search, name='member_search'),
]
from django.urls import path

from car.views import *

urlpatterns = [
    path('manage/', manage, name='manage'),
    path('car_add/', car_add, name='car_add'),
    path('car_edit/', car_edit, name='car_edit'),
    path('car_del/', car_del, name='car_del'),
    path('car_search/', car_search, name='car_search'),
    path('car_upload/', car_upload, name='car_upload'),
    path('car_download/', car_download, name='car_download'),
    path('car_index/', car_index, name='car_index'),
    path('car_monitor/', car_monitor, name='car_monitor'),
]
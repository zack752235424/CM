from django.urls import path

from fence.views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('fence_data/', fence_data, name='fence_data'),
    path('get_cars/', get_cars, name='get_cars'),
]
import time

from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection

# Create your views here.
from user.models import User


def index(request):
    rolename = User.objects.get(pk=request.session['user_id']).roles.first().rolename
    return render(request, 'index.html', {'rolename': rolename})


def map(request):
    a = 1
    return render(request, 'baidu_map.html')


def search(request):
    VIN = request.GET.get('VIN')
    r = get_redis_connection('default')
    car = r.geopos('car_offline', VIN)[0]
    if car:
        result = {'car': car + (VIN,)}
        return JsonResponse(result)
    car = r.geopos('car_online', VIN)[0]
    result = {'car': car + (VIN,)}
    return JsonResponse(result)

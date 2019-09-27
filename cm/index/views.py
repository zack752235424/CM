import time
import json

from django.http import JsonResponse
from django.shortcuts import render
from django_redis import get_redis_connection
from dwebsocket.decorators import accept_websocket

# Create your views here.
from user.models import User


def index(request):
    rolename = User.objects.get(pk=request.session['user_id']).roles.first().rolename
    return render(request, 'index.html', {'rolename': rolename})


def map(request):
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


@accept_websocket
def chat(request):
    if request.is_websocket():
        while True:
            r = get_redis_connection('default')
            messages = {}
            messages['car_online'] = []
            messages['car_offline'] = []
            messages['car_warning'] = []
            car_online = r.zrange('car_online', 0, -1)
            if car_online:
                for item in car_online:
                    car = r.geopos('car_online', item.decode('utf-8'))
                    messages['car_online'].append([car[0][0], car[0][1], item.decode('utf-8')])
            car_offline = r.zrange('car_offline', 0, -1)
            if car_offline:
                for item in car_offline:
                    cars = r.geopos('car_offline', item.decode('utf-8'))
                    messages['car_offline'].append([cars[0][0], cars[0][1], item.decode('utf-8')])
            car_warning = r.zrange('car_warning', 0, -1)
            if car_warning:
                for item in car_warning:
                    cars = r.geopos('car_warning', item.decode('utf-8'))
                    messages['car_warning'].append([cars[0][0], cars[0][1], item.decode('utf-8')])
            messages = json.dumps(messages)
            request.websocket.send(messages.encode())  # 发送给前段的数据
            time.sleep(10)


def error(request):
    return render(request, 'error.html')

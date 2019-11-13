import time
import json

from django.http import JsonResponse
from django.shortcuts import render
from dwebsocket.decorators import accept_websocket
from django_redis import get_redis_connection

# Create your views here.
from car.models import Car


def index(request):
    return render(request, 'fence.html')


@accept_websocket
def fence_data(request):
    if request.is_websocket():
        r = get_redis_connection('default')
        VINS = request.websocket.wait().decode('utf-8').split(',')  # 需要围栏的设备
        while True:
            messages = []
            car_online = r.zrange('car_online', 0, -1)
            if car_online:
                for item in car_online:
                    if item.decode('utf-8') in VINS:
                        car = r.geopos('car_online', item.decode('utf-8'))
                        messages.append([car[0][0], car[0][1], item.decode('utf-8')])
            car_offline = r.zrange('car_offline', 0, -1)
            if car_offline:
                for item in car_offline:
                    if item.decode('utf-8') in VINS:
                        cars = r.geopos('car_offline', item.decode('utf-8'))
                        messages.append([cars[0][0], cars[0][1], item.decode('utf-8')])
            car_warning = r.zrange('car_warning', 0, -1)
            if car_warning:
                for item in car_warning:
                    if item.decode('utf-8') in VINS:
                        cars = r.geopos('car_warning', item.decode('utf-8'))
                        messages.append([cars[0][0], cars[0][1], item.decode('utf-8')])
            messages = json.dumps(messages)
            request.websocket.send(messages.encode())  # 发送给前端的数据
            time.sleep(10)


def get_cars(request):
    cars = Car.objects.all()
    result = []
    deptlist = list(set(cars.values_list('dept')))
    [result.append({'title': deptlist[i][0], 'id': [i+1], 'children':[{'title': item[0], 'id': item[1]} for item in cars.filter(dept=deptlist[i][0]).values_list('VIN', 'id')]}) for i in range(len(deptlist))]
    return JsonResponse(result, safe=False)

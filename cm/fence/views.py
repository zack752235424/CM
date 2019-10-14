import time
import json

from django.shortcuts import render
from dwebsocket.decorators import accept_websocket
from django_redis import get_redis_connection

# Create your views here.


def index(request):
    return render(request, 'fence.html')


@accept_websocket
def fence_data(request):
    if request.is_websocket():
        r = get_redis_connection('default')
        while True:
            messages = []
            car_online = r.zrange('car_online', 0, -1)
            if car_online:
                for item in car_online:
                    car = r.geopos('car_online', item.decode('utf-8'))
                    messages.append([car[0][0], car[0][1], item.decode('utf-8')])
            car_offline = r.zrange('car_offline', 0, -1)
            if car_offline:
                for item in car_offline:
                    cars = r.geopos('car_offline', item.decode('utf-8'))
                    messages.append([cars[0][0], cars[0][1], item.decode('utf-8')])
            car_warning = r.zrange('car_warning', 0, -1)
            if car_warning:
                for item in car_warning:
                    cars = r.geopos('car_warning', item.decode('utf-8'))
                    messages.append([cars[0][0], cars[0][1], item.decode('utf-8')])
            messages = json.dumps(messages)
            request.websocket.send(messages.encode())  # 发送给前端的数据
            time.sleep(10)

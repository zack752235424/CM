import json

import time
from threading import Timer

from channels.generic.websocket import WebsocketConsumer
from django_redis import get_redis_connection

# 'ws://127.0.0.1:8000/ws/send_data'


class ChatConsumer(WebsocketConsumer):
    is_on = True

    def connect(self):
        self.accept()
        self.conti()

    def receive(self, text_data=None, bytes_data=None):
        pass

    def disconnect(self, close_code):
        # Called when the socket closes
        self.is_on = False

    def conti(self):
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
        self.send(messages)
        if self.is_on:
            Timer(10, self.conti).start()

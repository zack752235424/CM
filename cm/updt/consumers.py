import json

import time
from channels.generic.websocket import WebsocketConsumer
from django_redis import get_redis_connection

# 'ws://127.0.0.1:8000/ws/send_data'


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print('连接成功')
        r = get_redis_connection('default')
        messages = {}
        messages['car_online'] = []
        messages['car_offline'] = []
        car_online = r.zrange('car_online', 0, -1)
        if car_online:
            for item in car_online:
                car = r.geopos('car_online', item.decode('utf-8'))
                messages['car_online'].append([car[0], car[1], item])
        car_offline = r.zrange('car_offline', 0, -1)
        if car_offline:
            for item in car_offline:
                cars = r.geopos('car_offline', item.decode('utf-8'))
                messages['car_offline'].append([cars[0][0], cars[0][1], item.decode('utf-8')])
        messages = json.dumps(messages)
        print(messages)
        self.send(messages)

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        if text_data == 'ping':
            pass

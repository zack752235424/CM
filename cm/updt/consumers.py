import time
from channels.generic.websocket import WebsocketConsumer
import json

# 'ws://127.0.0.1:8000/ws/send_data'


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        mess = '232302fe544c474633443934324a484c303030303301016f13030c0f1718310f171800f018ffa1f308582a0000000000000f171800fa18ffa1f308592a0000000000000f1718010418ffa1f3085a2a0000000000000f1718010e18ffa1f3085b2a0000000000000f1718011818ffa1f3085c2a0000000000000f1718012218ffa1f3085d2a0000000000000f1718012c18ffa1f3085e2a0000000000000f1718013618ffa1f3085f2a0000000000000f1718014018ffa1f308602a0000000000000f1718014a18ffa1f308612a0000000000000f1718015418ffa1f308622a0000000000000f1718015e18ffa1f308632a0000000000000f1718016818ffa1f308642a0000000000000f1718017218ffa1f308652a0000000000000f1718017c18ffa1f308662a0000000000000f1718018618ffa1f308672a0000000000000f1718019018ffa1f308682a0000000000000f1718019a18ffa1f308692a0000000000000f171801a418ffa1f3086a2a0000000000000f171801ae18ffa1f3086b2a00000000000052'
        print(text_data)
        # text_data_json = json.loads(text_data)
        # message = '运维咖啡吧：' + text_data_json['message']
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

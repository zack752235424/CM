from django.urls import path
from updt.consumers import ChatConsumer

websocket_urlpatterns = [
    path('', ChatConsumer),
]
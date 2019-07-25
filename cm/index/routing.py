from django.urls import path

from index.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/', ChatConsumer),
]
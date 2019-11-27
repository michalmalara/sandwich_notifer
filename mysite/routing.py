from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from home.consumers import NoseyConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/", NoseyConsumer),
    ])
})
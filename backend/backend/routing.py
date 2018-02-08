from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url

from chat.authentication import JWTAuthMiddlewareStack
from chat.consumers import PrivateChatConsumer, UserEventsConsumer

application = ProtocolTypeRouter({

    # WebSocket chat handler
    "websocket": JWTAuthMiddlewareStack(
        URLRouter([
            url("^private_chat/$", PrivateChatConsumer),
            url("^user/$", UserEventsConsumer),
        ])
    ),
})
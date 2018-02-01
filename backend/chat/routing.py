from channels.routing import route
from chat.consumers import start_private_chat, private_chat_send_message, end_private_chat, user_connect, user_message, \
    user_disconnect

channel_routing = [
    route("websocket.connect", start_private_chat, path=r'^/private_chat$'),
    route("websocket.receive", private_chat_send_message, path=r'^/private_chat$'),
    route("websocket.disconnect", end_private_chat, path=r'^/private_chat$'),

    route("websocket.connect", user_connect, path=r'^/user$'),
    route("websocket.receive", user_message, path=r'^/user$'),
    route("websocket.disconnect", user_disconnect, path=r'^/user'),

]

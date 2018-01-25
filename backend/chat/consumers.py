import json
from channels import Group
from channels.auth import channel_session_user_from_http
from channels.sessions import channel_session
from urllib.parse import parse_qs
from utils.channels_token import rest_token_user

# Connected to websocket.connect
@rest_token_user
def ws_connect(message):
    # Accept connection
    message.reply_channel.send({"accept": True})
    # Add them to the right group
    Group("chat-%s" % message.user.username[0]).add(message.reply_channel)


# Connected to websocket.receive
@rest_token_user
def ws_message(message):

    Group("chat-%s" % message.user.username[0]).send({
        "text": message['text'],
    })

# Connected to websocket.disconnect
@rest_token_user
def ws_disconnect(message):
    Group("chat-%s" % message.user.username[0]).discard(message.reply_channel)



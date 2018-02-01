import datetime
import json

from backend.settings import _redis as r
from channels import Group, Channel
from channels.auth import channel_session_user_from_http
from channels.handler import AsgiRequest
from channels.sessions import channel_session, enforce_ordering
from urllib.parse import parse_qs

from django.db.models import Q
from rest_framework.exceptions import AuthenticationFailed

from chat.models import PrivateChat
from users.models import Person, Friend
from utils.channels import jwt_initial_auth, user_from_session, add_second_user
from rest_framework.settings import api_settings

LAST_MESSAGE = 'last_message'
PRIVATE_CHAT = 'private_chat'


@channel_session
@jwt_initial_auth
def user_connect(message):
    print('user connection init')
    message.reply_channel.send({'accept': True})
    Group(f'user_{message.user.id}').add(message.reply_channel)


@channel_session
@user_from_session
def user_message(message):
    print('user message')
    Group(f'user_{message.user.id}').send({'text': json.dumps({'text': message['text']})})


@channel_session
@user_from_session
def user_disconnect(message):
    print('user disconnect')
    Group(f'user_{message.user.id}').discard(message.reply_channel)


def get_private_chat(from_user, to_user):
    one, two = (from_user, to_user) if from_user < to_user else (to_user, from_user)
    one, two = Person.objects.get(pk=one), Person.objects.get(pk=two)
    pc, created = PrivateChat.objects.get_or_create(first_user=one, second_user=two)
    return pc, created


def get_from_user_to_user(message):
    return message.user.id, int(message.channel_session['to_user_id'])


@channel_session
@enforce_ordering
@jwt_initial_auth
@add_second_user
def start_private_chat(message):
    from_user, to_user = get_from_user_to_user(message)
    try:
        # check if both way friendship exists
        Friend.objects.get(first=from_user, second=to_user)
        Friend.objects.get(second=from_user, first=to_user)
        message.reply_channel.send({"accept": True})
    except Friend.DoesNotExist:
        message.reply_channel.send({"accept": False})
        return
    print(f'chat init from {from_user} to {to_user}')
    pc, created = get_private_chat(from_user, to_user)
    group_name = f'{PRIVATE_CHAT}_{pc.id}'
    try:
        group = Group(group_name)
        Group(group_name).add(message.reply_channel)
        print(len(Group(group_name).channel_layer.group_channels(group_name)))
        print('----')
    except Exception:
        print('exp')
        Group(group_name).discard(message.reply_channel)
        raise


@channel_session
@enforce_ordering
@user_from_session
def private_chat_send_message(message):
    from_user, to_user = get_from_user_to_user(message)
    pc, created = get_private_chat(from_user, to_user)
    print(f'chat {pc.id} {message["text"][:10]} from {from_user} to {to_user}')

    group_name = f'{PRIVATE_CHAT}_{pc.id}'
    try:
        group = Group(group_name)
        group.send({'text': json.dumps({'text': message['text']})})
        Group(f'user_{from_user}').send({'text': json.dumps(
            {'text': f'In chat {pc.id} from user{from_user} to user{to_user} was sent message {message["text"]}'})})
        Group(f'user_{to_user}').send({'text': json.dumps(
            {'text': f'In chat {pc.id} from user{from_user} to user{to_user} was sent message {message["text"]}'})})
        redis_last_message_name = f'{group_name}_{LAST_MESSAGE}'
        r.hmset(redis_last_message_name,
                {
                    'time': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%s'),
                    'text': message['text'],
                    'user_id': from_user
                }
                )

        print('----')
    except Exception:
        Group(group_name).discard(message.reply_channel)
        raise


@channel_session
@enforce_ordering
@user_from_session
def end_private_chat(message):
    from_user, to_user = get_from_user_to_user(message)
    pc, created = get_private_chat(from_user, to_user)
    group_name = f'{PRIVATE_CHAT}_{pc.id}'
    print(f'chat {pc.id} user {from_user} disconnected')
    group = Group(group_name)
    Group(group_name).discard(message.reply_channel)
    print('----')

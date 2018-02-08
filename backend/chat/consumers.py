import datetime
from copy import deepcopy
from time import sleep

from asgiref.sync import async_to_sync
from channels_redis.core import *
from backend.settings import _redis as r
from channels.generic.websocket import JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from django.db.models import Q
from chat.models import PrivateChat, PrivateMessage
from users.models import Person, Friend

LAST_MESSAGE = 'last_message'
PRIVATE_CHAT = 'private_chat'
MESSAGE = 'message'
USER = 'user'
TEXT_MESSAGE = 'text_message'


class PrivateChatConsumer(JsonWebsocketConsumer):

    def __init__(self, scope):
        scope['to_user'] = Person.objects.get(pk=scope['to_user_id'])
        super(PrivateChatConsumer, self).__init__(scope)

    def connect(self):
        from_user, to_user = self.scope['user'], self.scope['to_user']
        if from_user == to_user:
            self.accept()
        else:
            try:
                # check if both way friendship exists
                Friend.objects.get(first=from_user, second=to_user)
                Friend.objects.get(second=from_user, first=to_user)
                self.accept()
            except Friend.DoesNotExist:
                self.close('No such friendship')
                return
        print(f'chat init from {from_user} to {to_user}')
        pc, created = self._get_private_chat(from_user, to_user)
        group_name = f'{PRIVATE_CHAT}_{pc.id}'

        try:
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
        except Exception as e:
            print('Exeption on message in private chat' + str(e))
            self.async_group_discard(group_name, self.channel_name)
            raise

    def receive_json(self, content, **kwargs):
        from_user, to_user = self.scope['user'], self.scope['to_user']
        pc, created = self._get_private_chat(from_user, to_user)
        print(f'chat {pc.id} {content[:10]} from {from_user} to {to_user}')
        group_name = f'{PRIVATE_CHAT}_{pc.id}'
        try:
            time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
            data = {
                'action_type': TEXT_MESSAGE,
                'action': {
                    'chat': pc.id,
                    'user_id': from_user.id,
                    'time': time,
                    'text': content,
                }
            }
            chat_data = deepcopy(data)
            chat_data['type'] = 'chat.message'
            user_data = deepcopy(data)
            user_data['type'] = 'user.event'
            async_to_sync(self.channel_layer.group_send)(group_name, chat_data)
            async_to_sync(self.channel_layer.group_send)(f'user_{from_user.id}', user_data)
            async_to_sync(self.channel_layer.group_send)(f'user_{to_user.id}', user_data)

            redis_last_message_name = f'{group_name}_{LAST_MESSAGE}'
            r.hmset(redis_last_message_name,
                    {
                        'type': TEXT_MESSAGE,
                        'time': time,
                        'text': content,
                        'user_id': from_user.id
                    })
            PrivateMessage.objects.create(chat=pc, text=content, owner=from_user)
        except Exception as e:
            print('Exeption on message in private chat' + str(e))
            async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)
            raise

    def disconnect(self, message):
        from_user, to_user = self.scope['user'], self.scope['to_user']
        pc, created = self._get_private_chat(from_user, to_user)
        print(f'chat {pc.id} disconnected from {from_user} to {to_user}')
        group_name = f'{PRIVATE_CHAT}_{pc.id}'
        async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)

    def _get_private_chat(self, from_user, to_user):
        one, two = (from_user, to_user) if from_user.pk < to_user.pk else (to_user, from_user)
        pc, created = PrivateChat.objects.get_or_create(first_user=one, second_user=two)
        return pc, created

    def chat_message(self, event):
        self.send_json({
            'type': event['action_type'],
            'chat': event['action']['chat'],
            'user_id': event['action']['user_id'],
            'time': event['action']['time'],
            'text': event['action']['text'],
        })


class UserEventsConsumer(JsonWebsocketConsumer):

    def connect(self):
        print("user event connection")
        self.accept()
        user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(f'{USER}_{user.id}', self.channel_name)

    def receive_json(self, content, **kwargs):
        print('message to user event. WTF?')
        user = self.scope['user']
        async_to_sync(self.channel_layer.group_send)(f'{USER}_{user.id}',
                                                     {"type": "chat.message", "text": self.encode_json(content)}, )

    def disconnect(self, message):
        print('user event disconnect')
        user = self.scope['user']
        async_to_sync(self.channel_layer.group_discard)(f'{USER}_{user.id}', self.channel_name)

    def user_event(self, event):
        self.send_json({
            'type': event['action_type'],
            'action': event['action']
        })

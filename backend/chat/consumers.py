import datetime
import json
from copy import deepcopy
from time import sleep

from asgiref.sync import async_to_sync
from django.core.exceptions import ObjectDoesNotExist

from backend.settings import _redis as r
from channels.generic.websocket import JsonWebsocketConsumer
from django.db.models import Q

from chat.consts import LAST_MESSAGE, CHAT_TEXT_MESSAGE, PRIVATE_CHAT
from chat.models import PrivateChat, PrivateMessage
from users.consts import USER
from users.models import Person, Friend
from utils.django_annoying import get_object_or_None

CONSUMER_CHAT_MESSAGE = 'chat.message'
CONSUMER_USER_EVENT = 'user.event'


class PrivateChatConsumer(JsonWebsocketConsumer):

    def __init__(self, scope):
        to_user_id = scope.get('to_user_id')
        private_chat_id = scope.get('private_chat_id')
        try:
            if to_user_id:
                scope['to_user'] = Person.objects.get(pk=to_user_id)
            elif private_chat_id:
                pc = PrivateChat.objects.get(pk=private_chat_id)
                scope['private_chat'] = pc
                scope['to_user'] = pc.first_user if pc.first_user != scope['user'] else pc.second_user
            else:
                self.close()
        except ObjectDoesNotExist:
            self.close()
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
        group_name = f'{PRIVATE_CHAT}-{pc.id}'

        try:
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)
        except Exception as e:
            print('Exeption on message in private chat' + str(e))
            async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)
            raise

    def receive_json(self, content, **kwargs):
        from_user, to_user = self.scope['user'], self.scope['to_user']
        pc, created = self._get_private_chat(from_user, to_user)
        print(f'chat {pc.id} {content[:10]} from {from_user} to {to_user}')
        group_name = f'{PRIVATE_CHAT}-{pc.id}'
        try:
            pm = PrivateMessage.objects.create(chat=pc, text=content, owner=from_user)
            time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
            data = {
                'action_type': CHAT_TEXT_MESSAGE,
                'action': {
                    'id': pm.id,
                    'chat_type': PRIVATE_CHAT,
                    'chat': pc.id,
                    'owner': from_user.id,
                    'created_at': time,
                    'text': content,
                    'edited': False,
                    'edited_at': time
                }
            }
            chat_data = deepcopy(data)
            chat_data['type'] = CONSUMER_CHAT_MESSAGE
            from utils.websocket_utils import WebSocketEvent
            chat_data = WebSocketEvent(chat_data['action_type'], chat_data['action'], chat_data['type']).to_dict_flat()
            user_data = deepcopy(data)
            user_data['type'] = CONSUMER_USER_EVENT
            user_data = WebSocketEvent(user_data['action_type'], user_data['action'], user_data['type']).to_dict()
            async_to_sync(self.channel_layer.group_send)(group_name, chat_data)
            async_to_sync(self.channel_layer.group_send)(f'user-{from_user.id}', user_data)
            async_to_sync(self.channel_layer.group_send)(f'user-{to_user.id}', user_data)

            redis_last_message_name = f'{group_name}-{LAST_MESSAGE}'
            r.hmset(redis_last_message_name,
                    WebSocketEvent(data['action_type'], data['action']).to_dict_flat())
        except Exception as e:
            print('Exeption on message in private chat' + str(e))
            async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)
            raise e

    def disconnect(self, message):
        from_user, to_user = self.scope['user'], self.scope['to_user']
        pc, created = self._get_private_chat(from_user, to_user)
        print(f'chat {pc.id} disconnected from {from_user} to {to_user}')
        group_name = f'{PRIVATE_CHAT}-{pc.id}'
        async_to_sync(self.channel_layer.group_discard)(group_name, self.channel_name)

    def _get_private_chat(self, from_user, to_user):
        created = False
        if 'private_chat_id' in self.scope:
            pc = PrivateChat.objects.get(pk=self.scope['private_chat_id'])
        else:
            one, two = (from_user, to_user) if from_user.pk < to_user.pk else (to_user, from_user)
            pc, created = PrivateChat.objects.get_or_create(first_user=one, second_user=two)
        return pc, created

    def chat_message(self, event):
        print('chat message')
        event.pop('type')
        self.send_json(event)


class UserEventsConsumer(JsonWebsocketConsumer):
    def connect(self):
        print("user event connection")
        self.accept()
        user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(f'{USER}-{user.id}', self.channel_name)

    def receive_json(self, content, **kwargs):
        print('message to user event. WTF?')
        user = self.scope['user']
        async_to_sync(self.channel_layer.group_send)(f'{USER}-{user.id}',
                                                     {"type": "chat.message", "text": self.encode_json(content)}, )

    def disconnect(self, message):
        print('user event disconnect')
        user = self.scope['user']
        async_to_sync(self.channel_layer.group_discard)(f'{USER}-{user.id}', self.channel_name)

    def user_event(self, event):
        print('send user message')
        event.pop('type')
        self.send_json(event)

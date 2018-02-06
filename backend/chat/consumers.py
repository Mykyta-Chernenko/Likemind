import datetime

from channels.generic.websocket import JsonWebsocketConsumer
from django.db.models import Q
from chat.models import PrivateChat, PrivateMessage
from users.models import Person, Friend

LAST_MESSAGE = 'last_message'
PRIVATE_CHAT = 'private_chat'
MESSAGE = 'message'


class PrivateChatConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.accept()

    def receive_json(self, content, **kwargs):
        pass

    def disconnect(self, message, **kwargs):
        pass

# @channel_session
# @jwt_initial_auth
# def user_connect(message):
#     print('user connection init')
#     message.reply_channel.send({'accept': True})
#     Group(f'user_{message.user.id}').add(message.reply_channel)
#
#
# @channel_session
# @user_from_session
# def user_message(message):
#     print('user message')
#     Group(f'user_{message.user.id}').send({'text': json.dumps({'text': message['text']})})
#
#
# @channel_session
# @user_from_session
# def user_disconnect(message):
#     print('user disconnect')
#     Group(f'user_{message.user.id}').discard(message.reply_channel)
#
#
# def get_private_chat(from_user, to_user):
#     one, two = (from_user, to_user) if from_user.pk < to_user.pk else (to_user, from_user)
#     pc, created = PrivateChat.objects.get_or_create(first_user=one, second_user=two)
#     return pc, created
#
#
# def get_from_user_to_user(message):
#     return Person.objects.get(message.user.id), Person.objects.get(int(message.channel_session['to_user_id']))
#
#
# @channel_session
# @enforce_ordering
# @jwt_initial_auth
# @add_second_user
# def start_private_chat(message):
#     from_user, to_user = get_from_user_to_user(message)
#     try:
#         # check if both way friendship exists
#         Friend.objects.get(first=from_user, second=to_user)
#         Friend.objects.get(second=from_user, first=to_user)
#         message.reply_channel.send({"accept": True})
#     except Friend.DoesNotExist:
#         message.reply_channel.send({"accept": False})
#         return
#     print(f'chat init from {from_user} to {to_user}')
#     pc, created = get_private_chat(from_user, to_user)
#     group_name = f'{PRIVATE_CHAT}_{pc.id}'
#     try:
#         group = Group(group_name)
#         Group(group_name).add(message.reply_channel)
#         print(len(Group(group_name).channel_layer.group_channels(group_name)))
#         print('----')
#     except Exception:
#         print('exp')
#         Group(group_name).discard(message.reply_channel)
#         raise
#
#
# @channel_session
# @enforce_ordering
# @user_from_session
# def private_chat_send_message(message):
#     from_user, to_user = get_from_user_to_user(message)
#     pc, created = get_private_chat(from_user, to_user)
#     text = message['text']
#     print(f'chat {pc.id} {message["text"][:10]} from {from_user} to {to_user}')
#
#     group_name = f'{PRIVATE_CHAT}_{pc.id}'
#     try:
#         group = Group(group_name)
#         group.send({'text': json.dumps({'text': text})})
#         time = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
#         data = {'type': MESSAGE,
#                 'chat': pc.id,
#                 'user_id': from_user.id,
#                 'time': time,
#                 'text': text,
#                 }
#         Group(f'user_{from_user}').send({'text': json.dumps(
#             {'data': data})})
#         Group(f'user_{to_user}').send({'text': json.dumps(
#             {'data': data})})
#         redis_last_message_name = f'{group_name}_{LAST_MESSAGE}'
#         r.hmset(redis_last_message_name,
#                 {
#                     'time': time,
#                     'text': text,
#                     'user_id': from_user.id
#                 }
#                 )
#         PrivateMessage.objects.create(chat=pc, text=text, owner=from_user)
#         print('----')
#     except Exception:
#         Group(group_name).discard(message.reply_channel)
#         raise
#
#
# @channel_session
# @enforce_ordering
# @user_from_session
# def end_private_chat(message):
#     from_user, to_user = get_from_user_to_user(message)
#     pc, created = get_private_chat(from_user, to_user)
#     group_name = f'{PRIVATE_CHAT}_{pc.id}'
#     print(f'chat {pc.id} user {from_user} disconnected')
#     group = Group(group_name)
#     Group(group_name).discard(message.reply_channel)
#     print('----')

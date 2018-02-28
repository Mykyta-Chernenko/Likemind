import datetime
from copy import deepcopy

import channels
from rest_framework.permissions import IsAuthenticated

from backend.settings import _redis as r
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from chat.consts import REVERSE_CHAT_TYPES, LAST_MESSAGE
from chat.consumers import CONSUMER_CHAT_MESSAGE, CONSUMER_USER_EVENT
from files.consts import FILE_MESSAGE_FIELD, IMAGE_MESSAGE_FIELD, AUDIO_MESSAGE_FIELD, VIDEO_MESSAGE_FIELD
from files.models import ChatFile, ChatImage, ChatAudio, ChatVideo
from files.permissions import UserBelongToChat
from files.serializers import ChatFileSerializer, ChatImageSerializer, ChatAudioSerializer, ChatVideoSerializer
from utils.websocket_utils import WebSocketEvent, ActionType, ChatFileMessageAction, ChatImageMessageAction, \
    ChatAudioMessageAction, ChatVideoMessageAction

# TODO add file detail
class _ChatFileList(CreateAPIView, ListAPIView):
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated, UserBelongToChat]
    serializer_class = None
    queryset = None
    ActionType = None
    field = None

    def get_chat(self, **kwargs):
        if kwargs:
            model = kwargs.get('chat_model')
            model_id = kwargs.get('chat_id')
        else:
            model = self.kwargs.get('chat_model')
            model_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(model, pk=model_id)
        return ContentType.objects.get(app_label=chat._meta.app_label, model=chat._meta.model_name), model_id

    def create(self, request, *args, **kwargs):
        content_type, object_id = self.get_chat(**kwargs)
        if request.data:
            request.data['content_type'] = content_type.id
            request.data['object_id'] = object_id
        result = super(_ChatFileList, self).create(request, *args, **kwargs)
        time = datetime.datetime.now()
        chat = result.data['chat']
        file = result.data[self.field]
        id = result.data['id']
        content = f'file can be downloaded via link <a href="{file}"></a>'
        channel_layer = channels.layers.get_channel_layer()
        model = kwargs.get('chat_model')
        model_name = REVERSE_CHAT_TYPES[model]
        model_string_name = f'{model_name}-{object_id}'
        action = self.ActionType(id=id, chat_type=model_name, chat=chat['id'], owner=request.user.id,
                                 created_at=time, **{self.field: content})

        chat_data = WebSocketEvent(action, type=CONSUMER_CHAT_MESSAGE).to_dict_flat()
        user_data = WebSocketEvent(action, type=CONSUMER_USER_EVENT).to_dict()
        async_to_sync(channel_layer.group_send)(model_string_name, chat_data)
        chat = content_type.get_object_for_this_type(id=id)
        for user in chat.get_users():
            async_to_sync(channel_layer.group_send)(f'user-{user.id}', user_data)
        redis_last_message_name = f'{model_string_name}-{LAST_MESSAGE}'
        r.hmset(redis_last_message_name,
                WebSocketEvent(action).to_dict_flat())
        return result

    def perform_create(self, serializer):
        content_type, object_id = self.get_chat()
        serializer.save(content_type=content_type, object_id=object_id, owner=self.request.user)

    def get_queryset(self):
        content_type, object_id = self.get_chat()
        return self.queryset.filter(content_type=content_type, object_id=object_id)

    def list(self, request, *args, **kwargs):
        content_type, object_id = self.get_chat(**kwargs)
        self.queryset = self.queryset.filter(content_type=content_type, object_id=object_id)
        return super(_ChatFileList, self).list(request, *args, **kwargs)


class ChatFileList(_ChatFileList):
    '''
    post:
    requires chat-type from url (private-chat, group-chat, encrypted-private-chat) and its id.
    Creates file in the related chat

    get:
    requires chat-type from url (private-chat, group-chat, encrypted-private-chat) and its id.
    get list of files in the related chat
    '''
    serializer_class = ChatFileSerializer
    queryset = ChatFile.objects.all()
    ActionType = ChatFileMessageAction
    field = FILE_MESSAGE_FIELD


class ChatImageList(_ChatFileList):
    '''
    post:
    requires chat-type from url (private-chat, group-chat, encrypted-private-chat) and its id.
    Creates image in the related chat

    get:
    requires chat-type from url (private-chat, group-chat, encrypted-private-chat) and its id.
    get list of images in the related chat
    '''
    serializer_class = ChatImageSerializer
    queryset = ChatImage.objects.all()
    ActionType = ChatImageMessageAction
    field = IMAGE_MESSAGE_FIELD


class ChatAudioList(_ChatFileList):
    '''
    post:
    requires chat-type from url (private-chat, group-chat, encrypted-private-chat) and its id.
    Creates audio in the related chat

    get:
    requires chat-type from url (private-chat, group-chat, encrypted-private-chat) and its id.
    get list of audios in the related chat
    '''
    serializer_class = ChatAudioSerializer
    queryset = ChatAudio.objects.all()
    ActionType = ChatAudioMessageAction
    field = AUDIO_MESSAGE_FIELD


class ChatVideoList(_ChatFileList):
    '''

    post:
    requires chat-type from url (private-chat, group-chat, encrypted-private-chat) and its id.
    Creates video in the related chat

    get:
    requires chat-type from url (private-chat, group-chat, encrypted-private-chat) and its id.
    get list of videos in the related chat
    '''
    serializer_class = ChatVideoSerializer
    queryset = ChatVideo.objects.all()
    ActionType = ChatVideoMessageAction
    field = VIDEO_MESSAGE_FIELD

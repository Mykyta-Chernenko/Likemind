import json
from itertools import chain
from datetime import datetime
import channels
from asgiref.sync import async_to_sync
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView, \
    DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.utils.urls import replace_query_param

from chat.consts import MESSAGE_TYPE_TO_CHAT_TYPE, LAST_MESSAGE
from chat.consumers import CONSUMER_CHAT_MESSAGE, CONSUMER_USER_EVENT
from chat.models import PrivateChat, PrivateMessage, EncryptedPrivateMessage, GroupMessage
from chat.paginations import MessageListPagination
from chat.permissions import MessageBelongToChatAndUserIsOwner
from chat.serializers import PrivateChatSerializer, PrivateMessageSerializer, EncryptedPrivateMessageSerializer, \
    GroupMessageSerializer
from files.permissions import UserBelongToChatList
from files.serializers import ChatFileSerializer, ChatImageSerializer, ChatVideoSerializer, ChatAudioSerializer
from users.models import Person
from utils.consts import TIME_TZ_FORMAT
from utils.websocket_utils import WebSocketEvent, ChatTextMessageAction, ChatTextMessageUpdateAction, \
    ChatTextMessageDeleteAction
from backend.settings import r

MESSAGE_MAX_NUMBER = 1000
DEFAULT_MESSAGE_NUMBER = 20


# TODO add chats types that are left

class PrivateChatList(CreateAPIView, ListAPIView):
    '''
    get:
    gets list of private chats for the token user

    post:
    creates
    '''
    serializer_class = PrivateChatSerializer
    queryset = PrivateChat.objects.all()
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return PrivateChat.objects.filter(Q(first_user=self.request.user) | Q(second_user=self.request.user))

    def create(self, request, *args, **kwargs):
        try:
            first, second = request.user.id, int(request.data['second_user'])
        except (ValueError, TypeError):
            return Response(status=HTTP_400_BAD_REQUEST, data='second_user must be int')
        request.data['first_user'], request.data['second_user'] = (first, second) if first < second else (
            second, first)
        serializer = self.get_serializer(data=request.data)
        first_user_field = serializer.fields.fields['first_user']
        first_user_field.read_only = False
        first_user_field.queryset = Person.objects.all()
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class Message():
    permission_classes = [IsAuthenticated, MessageBelongToChatAndUserIsOwner]

    def get_queryset(self):
        chat_id = self.kwargs.get('chat_id')
        return self.queryset.filter(chat__pk=chat_id)


class MessageList(Message, CreateAPIView, ListAPIView):
    '''
    gets related chat by chat_id in url
    list: returns list of messages of related chat
    create: creates message in related chat
    '''
    pagination_class = MessageListPagination

    def perform_create(self, serializer):
        chat = get_object_or_404(MESSAGE_TYPE_TO_CHAT_TYPE[self.serializer_class.Meta.model], pk=self.kwargs['chat_id'])
        serializer.save(chat=chat, owner=self.request.user)


class _PrivateMessageList(MessageList):
    def get_queryset(self):
        queryset = super(MessageList, self).get_queryset().filter(
            Q(chat__first_user=self.request.user) | Q(chat__second_user=self.request.user))
        return queryset


class PrivateMessageList(_PrivateMessageList):
    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageSerializer


class EncryptedPrivateMessageList(_PrivateMessageList):
    queryset = EncryptedPrivateMessage.objects.all()
    serializer_class = EncryptedPrivateMessageSerializer


class GroupMessageList(MessageList):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer


class MessageDetail(UpdateAPIView, DestroyAPIView, RetrieveAPIView, Message):
    UpdateActionType = ChatTextMessageUpdateAction
    DeleteActionType = ChatTextMessageDeleteAction

    def get_chat_model(self):
        raise NotImplementedError

    def update(self, request, *args, **_kwargs):
        result = super(MessageDetail, self).update(request, *args, **_kwargs)
        obj = self.get_object()
        last = obj == self.queryset.latest('created_at')
        channel_layer = channels.layers.get_channel_layer()
        chat = obj.chat
        model_string_name = f'{chat.string_type()}-{chat.id}'
        action = self.UpdateActionType(id=obj.id, chat_type=chat.string_type(), chat=chat.id, owner=obj.owner.id,
                                       string_type=obj.string_type(), created_at=obj.created_at, text=obj.text,
                                       edited_at=obj.edited_at, edited=obj.edited)
        chat_data = WebSocketEvent(action, type=CONSUMER_CHAT_MESSAGE).to_dict_flat()
        async_to_sync(channel_layer.group_send)(model_string_name, chat_data)

        if last:
            user_data = WebSocketEvent(action, type=CONSUMER_USER_EVENT).to_dict()
            try:
                obj = self.queryset.latest('created_at')
            except ObjectDoesNotExist:
                obj = None
            new_action = self.DeleteActionType(id=obj.id, chat_type=chat.string_type(), chat=chat.id,
                                               owner=obj.owner.id,
                                               string_type=obj.string_type(), created_at=obj.created_at, text=obj.text,
                                               edited_at=obj.edited_at, edited=obj.edited)
            new_user_data = WebSocketEvent(new_action, type=CONSUMER_USER_EVENT).to_dict()
            for user in chat.get_users():
                for data in (user_data, new_user_data):
                    if data:
                        async_to_sync(channel_layer.group_send)(f'user-{user.id}', data)
            redis_last_message_name = f'{model_string_name}-{LAST_MESSAGE}'
            r.hmset(redis_last_message_name,
                    WebSocketEvent(new_action).to_dict_flat())

        return result

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        last = obj == self.queryset.latest('created_at')
        result = super(MessageDetail, self).destroy(request, *args, **kwargs)
        channel_layer = channels.layers.get_channel_layer()
        chat = obj.chat
        model_string_name = f'{chat.string_type()}-{chat.id}'
        action = self.DeleteActionType(id=obj.id, chat_type=chat.string_type(), chat=chat.id, owner=obj.owner.id,
                                       string_type=obj.string_type(), created_at=obj.created_at, text=obj.text,
                                       edited_at=obj.edited_at, edited=obj.edited)
        chat_data = WebSocketEvent(action, type=CONSUMER_CHAT_MESSAGE).to_dict_flat()
        async_to_sync(channel_layer.group_send)(model_string_name, chat_data)

        if last:
            user_data = WebSocketEvent(action, type=CONSUMER_USER_EVENT).to_dict()
            try:
                obj = self.queryset.latest('created_at')
                new_action = self.DeleteActionType(id=obj.id, chat_type=chat.string_type(), chat=chat.id,
                                                   owner=obj.owner.id,
                                                   string_type=obj.string_type(), created_at=obj.created_at,
                                                   text=obj.text, edited=obj.edited, edited_at=obj.edited_at)
                new_user_data = WebSocketEvent(new_action, type=CONSUMER_USER_EVENT).to_dict()
            except ObjectDoesNotExist:
                new_user_data = None
                new_action = None

            for user in chat.get_users():
                for data in (user_data, new_user_data):
                    if data:
                        async_to_sync(channel_layer.group_send)(f'user-{user.id}', data)
            redis_last_message_name = f'{model_string_name}-{LAST_MESSAGE}'
            if new_action:
                r.hmset(redis_last_message_name,
                        WebSocketEvent(new_action).to_dict_flat())
            else:
                r.delete(redis_last_message_name)
        return result


class PrivateMessageDetail(MessageDetail):
    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageSerializer


class EncryptedMessageDetail(MessageDetail):
    queryset = EncryptedPrivateMessage.objects.all()
    serializer_class = EncryptedPrivateMessageSerializer


class GroupMessageDetail(MessageDetail):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer


class ChatContent(ListAPIView):
    page_size = 20
    max_page_size = 200
    page_query_param = 'date_from'
    permission_classes = [IsAuthenticated, UserBelongToChatList]

    def get_chat(self, **kwargs):
        if kwargs:
            model = kwargs.get('chat_model')
            model_id = kwargs.get('chat_id')
        else:
            model = self.kwargs.get('chat_model')
            model_id = self.kwargs.get('chat_id')
        chat = get_object_or_404(model, pk=model_id)
        return chat

    def list(self, request, *args, **kwargs):
        chat = self.get_chat(**kwargs)
        messages = chat.message_set
        files = chat.files
        images = chat.images
        videos = chat.videos
        audios = chat.audios
        from_date = request.GET.get(self.page_query_param)
        page_size = self.page_size
        try:
            page_size = int(request.GET.get('page_size'))
            if page_size > self.max_page_size:
                page_size = self.max_page_size
            if page_size < self.page_size:
                page_size = self.page_size
        except (KeyError, ValueError, TypeError):
            pass
        content = [messages, files, images, videos, audios]
        if from_date:
            try:
                from_date = datetime.strptime(from_date, TIME_TZ_FORMAT)
            except ValueError:
                raise Response(status=status.HTTP_400_BAD_REQUEST,
                               data='wrong date format use %Y-%m-%dT%H:%M:%S.%fZ')

            for ind, object in enumerate(content):
                content[ind] = object.all().filter(created_at__gt=from_date)[:page_size]
        else:
            for ind, object in enumerate(content):
                content[ind] = object.all()[:page_size]
        messages, files, images, videos, audios = content
        _kwargs = {
            'many': True,
            'exclude_fields': 'chat'
        }

        messages_serialized = chat.message_set.model.get_serializer_class()(messages, **_kwargs).data
        files_serialized = ChatFileSerializer(files, **_kwargs).data
        images_serialized = ChatImageSerializer(images, **_kwargs).data
        videos_serialized = ChatVideoSerializer(videos, **_kwargs).data
        audios_serialized = ChatAudioSerializer(audios, **_kwargs).data
        result = sorted(
            chain(files_serialized, images_serialized, videos_serialized, audios_serialized, messages_serialized),
            key=lambda x: datetime.strptime(x['created_at'], TIME_TZ_FORMAT))[:page_size]

        count = len(result)
        date_from = result[-1]['created_at']
        if count < page_size:
            next = None
        else:
            url = self.request.build_absolute_uri()
            next = replace_query_param(url, self.page_query_param, date_from)
        data = {
            'next': next,
            'count': count,
            'results': result
        }
        return Response(data=data, status=HTTP_200_OK)

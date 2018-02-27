import json
from collections import OrderedDict
from itertools import chain

from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView, \
    DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.utils.urls import replace_query_param

from chat.consts import MESSAGE_TYPE_TO_CHAT_TYPE
from chat.models import PrivateChat, PrivateMessage, EncryptedPrivateMessage, GroupMessage
from chat.paginations import MessageListPagination
from chat.permissions import AllowMessageToOwner, MessageBelongToChat
from chat.serializers import PrivateChatSerializer, PrivateMessageSerializer, EncryptedPrivateMessageSerializer, \
    GroupMessageSerializer
from files.permissions import FileBelongToChat
from files.serializers import ChatFileSerializer, ChatImageSerializer, ChatVideoSerializer, ChatAudioSerializer
from utils.constants import TIME_TZ_FORMAT

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

    def perform_create(self, serializer):
        first, second = self.request.user, serializer.validated_data['second_user']
        first, serializer.validated_data['second_user'] = (first, second) if first.id < second.id else (second, first)
        serializer.save(first_user=first)


class Message():
    permission_classes = [IsAuthenticated, MessageBelongToChat]

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
    pass


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

    # TODO add next and previous page to pagination
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
        content = [messages, files, images, videos, audios]
        if from_date:
            try:
                from_date = datetime.strptime(from_date, TIME_TZ_FORMAT)
            except ValueError:
                raise Response(status=status.HTTP_400_BAD_REQUEST,
                               data='wrong date format use %Y-%m-%dT%H:%M:%S.%fZ')
            try:
                page_size = int(request.GET.get('page_size'))
                if page_size > self.max_page_size:
                    page_size = self.max_page_size
                if page_size < self.page_size:
                    page_size = self.page_size
            except (KeyError, ValueError, TypeError):
                pass
            for ind, object in enumerate(content):
                content[ind] = object.all().filter(created_at__gte=from_date)[:page_size]
        else:
            for ind, object in enumerate(content):
                content[ind] = object.all()[:page_size]
        messages, files, images, videos, audios = content
        messages_serialized = chat.message_set.model.get_serializer_class()(messages, many=True).data
        files_serialized = ChatFileSerializer(files, many=True).data
        images_serialized = ChatImageSerializer(images, many=True).data
        videos_serialized = ChatVideoSerializer(videos, many=True).data
        audios_serialized = ChatAudioSerializer(audios, many=True).data
        result = sorted(
            chain(files_serialized, images_serialized, videos_serialized, audios_serialized, messages_serialized),
            key=lambda x: datetime.strptime(x['created_at'], TIME_TZ_FORMAT))[:page_size]

        count = len(result)
        data_from = date_from = result[-1].created_at
        if count < 20:
            next = None
        else:
            url = self.request.build_absolute_uri()
            date_from = result[-1].created_at
            next = replace_query_param(url, self.page_query_param, data_from)
        data = {
            'next': next,
            'count': count,
            'results': result
        }
        return Response(data=data, status=HTTP_200_OK)

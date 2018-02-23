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

from chat.models import PrivateChat, PrivateMessage, EncryptedPrivateMessage, GroupMessage
from chat.paginations import MessageListPagination
from chat.permissions import AllowMessageToOwner
from chat.serializers import PrivateChatSerializer, PrivateMessageSerializer, EncryptedPrivateMessageSerializer, \
    GroupMessageSerializer
from files.serializers import ChatFileSerializer, ChatImageSerializer, ChatVideoSerializer, ChatAudioSerializer
from utils.constants import TIME_TZ_FORMAT

MESSAGE_MAX_NUMBER = 1000
DEFAULT_MESSAGE_NUMBER = 20


class PrivateChatList(CreateAPIView, ListAPIView):
    serializer_class = PrivateChatSerializer
    queryset = PrivateChat.objects.all()

    def get_queryset(self):
        return PrivateChat.objects.filter(Q(first_user=self.request.user) | Q(second_user=self.request.user))


class Message():
    def get_queryset(self):
        queryset = self.queryset.filter(chat__pk=self.kwargs['chat_id'])
        return queryset


class MessageList(CreateAPIView, ListAPIView, Message):
    pagination_class = MessageListPagination

    def perform_create(self, serializer):
        chat = get_object_or_404(self.serializer_class.Meta.model, pk=self.kwargs['chat_id'])
        serializer.save(chat=chat, owner=self.request.user)


class _PrivateMessageList(MessageList):

    def get_queryset(self):
        queryset = super(_PrivateMessageList, self).get_queryset().filter(
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
    permission_classes = [IsAuthenticated, AllowMessageToOwner]


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
        from_date = request.GET.get('from_date')
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
            for ind,object in enumerate(content):
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
        data = sorted(
            chain(files_serialized, images_serialized, videos_serialized, audios_serialized, messages_serialized),
            key=lambda x: datetime.strptime(x['created_at'], TIME_TZ_FORMAT))[:page_size]
        return Response(data=data, status=HTTP_200_OK)

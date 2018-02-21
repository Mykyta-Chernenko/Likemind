from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView, \
    DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from chat.models import PrivateChat, PrivateMessage, EncryptedPrivateMessage, GroupMessage
from chat.paginations import MessageListPagination
from chat.permissions import AllowMessageToOwner
from chat.serializers import PrivateChatSerializer, PrivateMessageSerializer, EncryptedPrivateMessageSerializer, \
    GroupMessageSerializer

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

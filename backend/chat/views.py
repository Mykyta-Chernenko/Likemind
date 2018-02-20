from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView, UpdateAPIView, RetrieveAPIView, \
    DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from chat.models import PrivateChat, PrivateMessage
from chat.permissions import AllowMessageToOwner
from chat.serializers import PrivateChatSerializer, PrivateMessageSerializer

MESSAGE_MAX_NUMBER = 1000
DEFAULT_MESSAGE_NUMBER = 20


class PrivateChatList(CreateAPIView, ListAPIView):
    serializer_class = PrivateChatSerializer
    queryset = PrivateChat.objects.all()

    def get_queryset(self):
        return PrivateChat.objects.filter(Q(first_user=self.request.user) | Q(second_user=self.request.user))


class PrivateMessageList(CreateAPIView, ListAPIView):
    serializer_class = PrivateMessageSerializer
    queryset = PrivateMessage.objects.all()

    def get_queryset(self):
        self.queryset = self.queryset.filter(
            Q(chat__pk=self.kwargs['chat_pk']) & (Q(chat__first_user=self.request.user) | Q(chat__second_user=self.request.user)))
        try:
            message_number = int(self.request.GET['message_number'])
            message_number = message_number if message_number <= MESSAGE_MAX_NUMBER else MESSAGE_MAX_NUMBER
            from_message_number = int(self.request.GET.get('from_message_number', 0))
        except (ValueError, KeyError):
            message_number = DEFAULT_MESSAGE_NUMBER
            from_message_number = 0
        return self.queryset[from_message_number: from_message_number + message_number]


class PrivateMessageDetail(UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    permission_classes = [IsAuthenticated, AllowMessageToOwner]
    queryset = PrivateMessage.objects.all()
    serializer_class = PrivateMessageSerializer

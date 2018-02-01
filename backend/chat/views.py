from django.db.models import Q
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated

from chat.models import PrivateChat
from chat.serializers import PrivateChatSerializer


class PrivateChatList(CreateAPIView, ListAPIView):
    serializer_class = PrivateChatSerializer
    queryset = PrivateChat.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PrivateChat.objects.filter(Q(first_user=self.request.user) | Q(second_user=self.request.user))


class PrivateMessageList(CreateAPIView, GenericAPIView):
    serializer_class = ''

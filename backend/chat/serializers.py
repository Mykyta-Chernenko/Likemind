import json
from collections import OrderedDict

from rest_framework import serializers

from chat.models import PrivateChat, PrivateMessage
from backend.settings import _redis as r
from chat.consumers import LAST_MESSAGE, PRIVATE_CHAT
from users.serializers import UserSerializer


class PrivateChatSerializer(serializers.ModelSerializer):
    first_user = UserSerializer()
    second_user = UserSerializer()

    class Meta:
        model = PrivateChat
        fields = ['id', 'first_user', 'second_user', 'creation']
        depth = 1

    def to_representation(self, instance):
        serialized = super(PrivateChatSerializer, self).to_representation(instance)
        redis_chat_last_message = f'{PRIVATE_CHAT}_{instance.id}_{LAST_MESSAGE}'
        exist = r.exists(redis_chat_last_message)
        last_message = {}
        if exist:
            last_message['text'] = r.hget(redis_chat_last_message, 'text').decode('utf-8')
            last_message['created_at'] = r.hget(redis_chat_last_message, 'created_at').decode('utf-8')
            last_message['owner'] = r.hget(redis_chat_last_message, 'owner').decode('utf-8')
        else:
            _last_message = instance.last_message()
            if _last_message:
                last_message = PrivateMessageSerializer(_last_message).data
        serialized['last_message'] = OrderedDict(last_message)
        return serialized


class PrivateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateMessage
        fields = ['owner', 'text', 'chat', 'created_at', 'edited', 'edited_at']

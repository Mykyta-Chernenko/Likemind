import json
from collections import OrderedDict

from rest_framework import serializers

from chat.models import PrivateChat
# from backend.settings import _redis as r
from chat.consumers import LAST_MESSAGE, PRIVATE_CHAT


class PrivateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChat
        fields = ['first_user', 'second_user', 'creation']
        depth = 1

    def to_representation(self, instance):
        serialized = super(PrivateChatSerializer, self).to_representation(instance)
        redis_chat_last_message = f'{PRIVATE_CHAT}_{instance.id}_{LAST_MESSAGE}'
        # exist = r.exists(redis_chat_last_message)
        last_message = {}
        # if exist:
        #     last_message['text'] = r.hget(redis_chat_last_message, 'text').decode('utf-8')
        #     last_message['time'] = r.hget(redis_chat_last_message, 'time').decode('utf-8')
        #     last_message['user_id'] = r.hget(redis_chat_last_message, 'user_id').decode('utf-8')
        serialized['last_message'] = OrderedDict(last_message)
        return serialized

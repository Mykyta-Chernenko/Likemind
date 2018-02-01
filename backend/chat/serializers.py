import json

from rest_framework import serializers

from chat.models import PrivateChat
from backend.settings import _redis as r
from chat.consumers import LAST_MESSAGE, PRIVATE_CHAT


class PrivateChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChat
        fields = ['first_user', 'second_user', 'creation']
        depth = 1

    def to_representation(self, instance):
        serialized = super(PrivateChatSerializer, self).to_representation(instance)
        last_message = r.hget(f'{PRIVATE_CHAT}_{instance.id}_{LAST_MESSAGE}', 'text')
        if last_message:
            last_message = last_message.decode('utf-8')
        else:
            last_message = 'no messages yet'
        serialized['last_message'] = json.dumps(last_message)
        return  serialized

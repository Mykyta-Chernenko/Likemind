import json
from collections import OrderedDict

from rest_framework import serializers

from chat.models import PrivateChat, PrivateMessage, EncryptedPrivateMessage, GroupMessage, EncryptedPrivateChat, \
    GroupChat
from backend.settings import _redis as r
from chat.consumers import LAST_MESSAGE, PRIVATE_CHAT
from users.serializers import UserSerializer


class MessageObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, PrivateMessage):
            serializer = PrivateMessageSerializer(value)
        elif isinstance(value, EncryptedPrivateMessage):
            serializer = EncryptedPrivateMessageSerializer(value)
        elif isinstance(value, GroupMessage):
            serializer = GroupMessageSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class ChatSerializer(serializers.ModelSerializer):
    last_message = MessageObjectRelatedField(read_only=True)

    class Meta:
        fields = ['id', 'creation', 'last_message', 'string_type']
        depth = 1


class PrivateChatSerializer(ChatSerializer):
    first_user = UserSerializer(short=True)
    second_user = UserSerializer(short=True)

    class Meta(ChatSerializer.Meta):
        model = PrivateChat
        fields = ChatSerializer.Meta.fields + ['first_user', 'second_user']
        depth = 0

    def __init__(self, *args, short=False, **kwargs):
        super(PrivateChatSerializer, self).__init__(*args, **kwargs)
        if short:
            if 'first_user' in self.fields:
                self.fields.pop('first_user')
            if 'second_user' in self.fields:
                self.fields.pop('second_user')


class EncryptedPrivateChatSerializer(ChatSerializer):
    class Meta(ChatSerializer.Meta):
        model = EncryptedPrivateChat
        fields = ChatSerializer.Meta.fields + ['keep_time']


class GroupChatSerializer(ChatSerializer):
    class Meta(ChatSerializer.Meta):
        model = GroupChat
        fields = ChatSerializer.Meta.fields + ['time']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'owner', 'text', 'chat', 'created_at', 'edited', 'edited_at']
        extra_kwargs = {
            'owner': {'read_only': True},
            'chat': {'read_only': True},
            'edited': {'read_only': True},
        }


class PrivateMessageSerializer(MessageSerializer):
    class Meta(MessageSerializer.Meta):
        model = PrivateMessage
        fields = MessageSerializer.Meta.fields


class EncryptedPrivateMessageSerializer(MessageSerializer):
    class Meta(MessageSerializer.Meta):
        model = EncryptedPrivateMessage
        fields = MessageSerializer.Meta.fields


class GroupMessageSerializer(MessageSerializer):
    class Meta(MessageSerializer.Meta):
        model = GroupMessage
        fields = MessageSerializer.Meta.fields

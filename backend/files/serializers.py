import json
from collections import OrderedDict
from copy import deepcopy

import os
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import empty

from chat.models import PrivateChat, PrivateMessage, GroupChat, EncryptedPrivateChat
from backend.settings import _redis as r
from chat.consumers import LAST_MESSAGE, PRIVATE_CHAT
from chat.serializers import PrivateChatSerializer, EncryptedPrivateChatSerializer, GroupChatSerializer
from files.models import ChatImage, ChatAudio, ChatVideo, ChatFile
from users.serializers import UserSerializer


class ChatObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, PrivateChat):
            serializer = PrivateChatSerializer(value, short=True)
        elif isinstance(value, EncryptedPrivateChat):
            serializer = EncryptedPrivateChatSerializer(value, short=True)
        elif isinstance(value, GroupChat):
            serializer = GroupChatSerializer(value, short=True)
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class _ChatFileSerializer(serializers.ModelSerializer):
    chat = ChatObjectRelatedField(read_only=True)

    class Meta:
        fields = ['id', 'chat', 'owner', 'description', 'created_at', 'string_type']
        extra_kwargs = {
            'owner': {'read_only': True}
        }


class ChatFileSerializer(_ChatFileSerializer):
    class Meta(_ChatFileSerializer.Meta):
        model = ChatFile
        fields = _ChatFileSerializer.Meta.fields + ['file']


class ChatImageSerializer(_ChatFileSerializer):
    class Meta(_ChatFileSerializer.Meta):
        model = ChatImage
        fields = _ChatFileSerializer.Meta.fields + ['image']


class ChatVideoSerializer(_ChatFileSerializer):
    class Meta(_ChatFileSerializer.Meta):
        model = ChatVideo
        fields = _ChatFileSerializer.Meta.fields + ['video']


class ChatAudioSerializer(_ChatFileSerializer):
    class Meta(_ChatFileSerializer.Meta):
        model = ChatAudio
        fields = _ChatFileSerializer.Meta.fields + ['audio']


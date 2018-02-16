import json
from collections import OrderedDict

from rest_framework import serializers
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


class ChatFileSerializer(serializers.ModelSerializer):
    chat = ChatObjectRelatedField(read_only=True)

    class Meta:
        model = ChatFile
        fields = ['file', 'chat']


class ChatImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatImage
        fields = ['chat', 'image']


class ChatVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatVideo
        fields = ['chat', 'video']


class ChatAudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatAudio
        fields = ['chat', 'audio']

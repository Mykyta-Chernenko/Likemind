import json
from collections import OrderedDict

from rest_framework import serializers

from chat.models import PrivateChat, PrivateMessage
from backend.settings import _redis as r
from chat.consumers import LAST_MESSAGE, PRIVATE_CHAT
from files.models import ChatImage, ChatAudio, ChatVideo, ChatFile
from users.serializers import UserSerializer


class ChatFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatFile
        fields = ['object_id', 'content_type', 'file']


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

from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers
from chat.models import PrivateChat, PrivateMessage, EncryptedPrivateMessage, GroupMessage, EncryptedPrivateChat, \
    GroupChat
from files.models import ChatImage, ChatAudio, ChatVideo, ChatFile
from users.models import Person
from users.serializers import UserSerializer
from utils.drf_mixins import SerializerFieldsMixin


class MessageObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        text_models = [PrivateMessage, EncryptedPrivateMessage, GroupMessage]
        file_models = [ChatFile, ChatImage, ChatAudio, ChatVideo]
        for model in text_models:
            if isinstance(value, model):
                return model.get_serializer_class()(value, exclude_fields='chat').data
        for model in file_models:
            if isinstance(value, model):
                return model.get_serializer_class()(value, exclude_fields='chat').data

        raise Exception('Unexpected type of tagged object')


class ChatSerializer(QueryFieldsMixin, SerializerFieldsMixin, serializers.ModelSerializer):
    last_message = MessageObjectRelatedField(read_only=True)
    images = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    audios = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    videos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    files = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        fields = ['id', 'creation', 'last_message', 'string_type', 'images', 'audios', 'videos', 'files']
        depth = 2


class _PrivateChatSeriliazer(ChatSerializer):
    first_user = serializers.PrimaryKeyRelatedField(read_only=True)
    second_user = serializers.PrimaryKeyRelatedField(queryset=Person.objects.all())

    class Meta:
        fields = ChatSerializer.Meta.fields + ['first_user', 'second_user']

    def __init__(self, *args, short=False, **kwargs):
        super(_PrivateChatSeriliazer, self).__init__(*args, **kwargs)


class PrivateChatSerializer(_PrivateChatSeriliazer):
    class Meta(_PrivateChatSeriliazer.Meta):
        model = PrivateChat
        fields = _PrivateChatSeriliazer.Meta.fields
        depth = 0

    def validate(self, attrs):
        instance = PrivateChat(**attrs)
        instance.clean()
        return attrs


class EncryptedPrivateChatSerializer(_PrivateChatSeriliazer):
    class Meta(ChatSerializer.Meta):
        model = EncryptedPrivateChat
        fields = _PrivateChatSeriliazer.Meta.fields + ['keep_time']

    def validate(self, attrs):
        instance = EncryptedPrivateChat(**attrs)
        instance.clean()
        return attrs


class GroupChatSerializer(ChatSerializer):
    class Meta(ChatSerializer.Meta):
        model = GroupChat
        fields = ChatSerializer.Meta.fields + ['time']


class MessageSerializer(QueryFieldsMixin, SerializerFieldsMixin, serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'owner', 'text', 'chat', 'created_at', 'edited', 'edited_at', 'string_type']
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

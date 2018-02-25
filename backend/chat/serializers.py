from rest_framework import serializers
from chat.models import PrivateChat, PrivateMessage, EncryptedPrivateMessage, GroupMessage, EncryptedPrivateChat, \
    GroupChat
from files.models import ChatImage, ChatAudio, ChatVideo, ChatFile
from users.serializers import UserSerializer


class MessageObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        models = [PrivateMessage, EncryptedPrivateMessage, GroupMessage, ChatFile, ChatImage, ChatAudio, ChatVideo]
        for model in models:
            if isinstance(value, model):
                # TODO add short
                return model.get_serializer_class()(value).data

        raise Exception('Unexpected type of tagged object')


class ChatSerializer(serializers.ModelSerializer):
    last_message = MessageObjectRelatedField(read_only=True)
    images = serializers.PrimaryKeyRelatedField(
        queryset=ChatImage.objects.all(), many=True
    )
    audios = serializers.PrimaryKeyRelatedField(
        queryset=ChatAudio.objects.all(), many=True
    )
    videos = serializers.PrimaryKeyRelatedField(
        queryset=ChatVideo.objects.all(), many=True
    )
    files = serializers.PrimaryKeyRelatedField(
        queryset=ChatFile.objects.all(), many=True
    )

    class Meta:
        fields = ['id', 'creation', 'last_message', 'string_type', 'images', 'audios', 'videos', 'files']
        depth = 2


class _PrivateChatSeriliazer(ChatSerializer):
    first_user = UserSerializer(short=True)
    second_user = UserSerializer(short=True)

    class Meta:
        fields = ChatSerializer.Meta.fields + ['first_user', 'second_user']

    def __init__(self, *args, short=False, **kwargs):
        super(_PrivateChatSeriliazer, self).__init__(*args, **kwargs)
        if short:
            if 'first_user' in self.fields:
                self.fields.pop('first_user')
            if 'second_user' in self.fields:
                self.fields.pop('second_user')


class PrivateChatSerializer(_PrivateChatSeriliazer):
    class Meta(_PrivateChatSeriliazer.Meta):
        model = PrivateChat
        fields = _PrivateChatSeriliazer.Meta.fields
        depth = 0


class EncryptedPrivateChatSerializer(_PrivateChatSeriliazer):
    class Meta(ChatSerializer.Meta):
        model = EncryptedPrivateChat
        fields = _PrivateChatSeriliazer.Meta.fields + ['keep_time']


class GroupChatSerializer(ChatSerializer):
    class Meta(ChatSerializer.Meta):
        model = GroupChat
        fields = ChatSerializer.Meta.fields + ['time']


class MessageSerializer(serializers.ModelSerializer):
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

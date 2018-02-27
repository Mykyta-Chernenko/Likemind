from drf_queryfields import QueryFieldsMixin
from rest_framework import serializers
from chat.models import PrivateChat, GroupChat, EncryptedPrivateChat
from chat.serializers import PrivateChatSerializer, EncryptedPrivateChatSerializer, GroupChatSerializer
from files.models import ChatImage, ChatAudio, ChatVideo, ChatFile
from utils.drf_mixins import SerializerFieldsMixin


class ChatObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        """
        Serialize bookmark instances using a bookmark serializer,
        and note instances using a note serializer.
        """
        if isinstance(value, PrivateChat):
            serializer = PrivateChatSerializer(value, exclude_fields='first_user,second_user')
        elif isinstance(value, EncryptedPrivateChat):
            serializer = EncryptedPrivateChatSerializer(value, exclude_fields='first_user,second_user')
        elif isinstance(value, GroupChat):
            serializer = GroupChatSerializer(value, exclude_fields='first_user,second_user')
        else:
            raise Exception('Unexpected type of tagged object')

        return serializer.data


class _ChatFileSerializer(QueryFieldsMixin, SerializerFieldsMixin, serializers.ModelSerializer):
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

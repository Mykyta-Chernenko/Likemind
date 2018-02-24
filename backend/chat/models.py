import datetime
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

from files.models import ChatFile, ChatVideo, ChatImage, ChatAudio
from users.models import Person
from backend.settings import _redis as r
from utils.models_methods import _string_type


class AbstractMessage(models.Model):
    text = models.TextField(max_length=1000)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.edited_at and self.created_at and self.edited_at != self.created_at:
            self.edited = True
        return super(AbstractMessage, self).save(*args, **kwargs)

    @classmethod
    def string_type(cls):
        return _string_type(cls)

    @classmethod
    def get_action_class(cls):
        from utils.websocket_utils import ChatTextMessageAction
        return ChatTextMessageAction

    @classmethod
    def get_serializer_class(cls):
        raise NotImplementedError('override get_serializer_class')


class AbstartPrivateMessage(AbstractMessage):
    class Meta(AbstractMessage.Meta):
        abstract = True


class PrivateMessage(AbstractMessage):
    chat = models.ForeignKey('PrivateChat', on_delete=models.CASCADE, related_name='message_set')

    def clean(self):
        pc = self.chat
        if not (self.owner == pc.first_user or self.owner == pc.second_user):
            raise ValidationError("User doesn't belong to chat")
        super(PrivateMessage, self).clean()

    @classmethod
    def get_serializer_class(cls):
        from chat.serializers import PrivateMessageSerializer
        return PrivateMessageSerializer


class EncryptedPrivateMessage(AbstractMessage):
    chat = models.ForeignKey('EncryptedPrivateChat', on_delete=models.CASCADE, related_name='message_set')

    @property
    def should_delete(self):
        return self.created_at + self.chat.keep_time < datetime.datetime.now()

    def clean(self):
        pc = self.chat
        if not (self.owner == pc.first_user or self.owner == pc.second_user):
            raise ValidationError("User doesn't belong to chat")
        super(EncryptedPrivateMessage, self).clean()

    @classmethod
    def get_serializer_class(cls):
        from chat.serializers import EncryptedPrivateMessageSerializer
        return EncryptedPrivateMessageSerializer


class GroupMessage(AbstractMessage):
    chat = models.ForeignKey('GroupChat', on_delete=models.CASCADE, related_name='message_set')

    @classmethod
    def get_serializer_class(cls):
        from chat.serializers import GroupMessageSerializer
        return GroupMessageSerializer


class AbstractChat(models.Model):
    creation = models.DateTimeField(auto_now_add=True)
    last_use = models.DateTimeField(auto_now=True)
    files = GenericRelation(ChatFile)
    videos = GenericRelation(ChatVideo)
    images = GenericRelation(ChatImage)
    audios = GenericRelation(ChatAudio)

    class Meta:
        abstract = True

    def last_message(self):
        from chat.consts import LAST_MESSAGE, REVERSE_CHAT_TYPES, CHAT_TYPE_TO_MESSAGE_TYPE, CHAT_TYPES
        model_string_name = REVERSE_CHAT_TYPES[self._meta.model]
        redis_chat_last_message = f'{model_string_name}_{self.id}_{LAST_MESSAGE}'
        exist = r.exists(redis_chat_last_message)
        from chat.consts import TEXT_MESSAGE_FIELD
        from files.consts import IMAGE_MESSAGE_FIELD, AUDIO_MESSAGE_FIELD, VIDEO_MESSAGE_FIELD, FILE_MESSAGE_FIELD, \
            file_model_from_field
        if exist:
            last_message = {}
            message_type_variants = [TEXT_MESSAGE_FIELD, IMAGE_MESSAGE_FIELD,
                                     AUDIO_MESSAGE_FIELD, VIDEO_MESSAGE_FIELD,
                                     FILE_MESSAGE_FIELD]
            last_message_type = None
            for type in message_type_variants:
                if r.hexists(redis_chat_last_message, type):
                    last_message_type = type
                    break
            if not last_message_type:
                print("can't distinguish last message type")
                return None

            def populate_dict_from_redis(dct, *args):
                for key in args:
                    dct[key] = r.hget(redis_chat_last_message, key).decode('utf-8')

            populate_dict_from_redis(last_message, last_message_type, 'created_at', 'owner')

            if last_message_type is TEXT_MESSAGE_FIELD:
                populate_dict_from_redis(last_message, 'edited', 'edited_at')
            try:
                last_message['owner'] = Person.objects.get(pk=last_message['owner'])
            except Person.DoesNotExist:
                return None
            result = None
            if last_message_type is TEXT_MESSAGE_FIELD:
                result = CHAT_TYPE_TO_MESSAGE_TYPE[self._meta.model](**last_message)
            else:
                result = file_model_from_field[last_message_type](**last_message)

            return result
        else:
            message_queryobject_field = {
                self.message_set: TEXT_MESSAGE_FIELD, self.files: FILE_MESSAGE_FIELD,
                self.videos: VIDEO_MESSAGE_FIELD, self.audios: AUDIO_MESSAGE_FIELD,
                self.images: IMAGE_MESSAGE_FIELD
            }
            for query_object, field in message_queryobject_field.items():
                if query_object.exists():
                    obj = query_object.latest('created_at')
                    model_name = REVERSE_CHAT_TYPES[obj.chat._meta.model]
                    extra_fields = {field: getattr(obj, field)}
                    if field == TEXT_MESSAGE_FIELD:
                        extra_fields['edited'] = getattr(obj, 'edited')
                        extra_fields['edited_at'] = getattr(obj, 'edited_at')
                    action = obj.get_action_class()(
                        id=obj.id, chat_type=model_name, chat=obj.chat.id,
                        owner=obj.owner, created_at=obj.created_at,
                        **extra_fields)
                    model_string_name = f'{model_string_name}-{obj.chat.id}'
                    redis_last_message_name = f'{model_string_name}-{LAST_MESSAGE}'
                    from utils.websocket_utils import WebSocketEvent
                    r.hmset(redis_last_message_name, WebSocketEvent(action).to_dict_flat())
                    return obj

    def get_users(self):
        raise NotImplementedError

    @classmethod
    def get_serializer_class(cls):
        raise NotImplementedError('override get_serializer')

    @classmethod
    def string_type(self):
        return _string_type(self)


class AbstractPrivateChat(AbstractChat):
    first_user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='%(class)s_first_set')
    second_user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='%(class)s_second_set')

    class Meta(AbstractChat.Meta):
        abstract = True
        unique_together = ('first_user', 'second_user')

    def __str__(self):
        return f' {self.first_user} and {self.second_user}'

    def clean(self):
        if self.first_user and self.second_user and self.first_user.id > self.second_user.id:
            raise ValidationError('The first user must have lower id than the second. Swap users')

    def get_users(self):
        return [self.first_user, self.second_user]


class PrivateChat(AbstractPrivateChat):
    class Meta(AbstractChat.Meta):
        verbose_name = 'private-chat'

    @classmethod
    def get_serializer_class(cls):
        from chat.serializers import PrivateChatSerializer
        return PrivateChatSerializer


class EncryptedPrivateChat(AbstractPrivateChat):
    keep_time = models.DurationField(default=datetime.timedelta(minutes=1))

    class Meta(AbstractPrivateChat.Meta):
        verbose_name = 'encrypted-private-chat'

    @classmethod
    def get_serializer_class(cls):
        from chat.serializers import EncryptedPrivateMessageSerializer
        return EncryptedPrivateMessageSerializer


class GroupChat(AbstractChat):
    name = models.CharField(max_length=255)

    class Meta(AbstractChat.Meta):
        verbose_name = 'group-chat'

    def get_users(self):
        return self.user_set.all()

    @classmethod
    def get_serializer_class(cls):
        from chat.serializers import GroupChatSerializer
        return GroupChatSerializer


class GroupChatUser:
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)

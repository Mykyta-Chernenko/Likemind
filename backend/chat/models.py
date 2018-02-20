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
    def string_type(self):
        return _string_type(self)


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


class GroupMessage(AbstractMessage):
    chat = models.ForeignKey('GroupChat', on_delete=models.CASCADE, related_name='message_set')


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
        if exist:
            last_message = {}
            last_message['text'] = r.hget(redis_chat_last_message, 'text').decode('utf-8')
            last_message['created_at'] = r.hget(redis_chat_last_message, 'created_at').decode('utf-8')
            owner = r.hget(redis_chat_last_message, 'owner').decode('utf-8')
            try:
                last_message['owner'] = Person.objects.get(pk=owner)
            except Person.DoesNotExist:
                return None
            message = CHAT_TYPE_TO_MESSAGE_TYPE[self._meta.model](**last_message)
            return message
        else:
            try:
                return self.message_set.latest('created_at')
            except ObjectDoesNotExist:
                return None

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


class PrivateChat(AbstractPrivateChat):
    class Meta(AbstractChat.Meta):
        verbose_name = 'private-chat'


class EncryptedPrivateChat(AbstractPrivateChat):
    keep_time = models.DurationField(default=datetime.timedelta(minutes=1))

    class Meta(AbstractPrivateChat.Meta):
        verbose_name = 'encrypted-private-chat'


class GroupChat(AbstractChat):
    name = models.CharField(max_length=255)

    class Meta(AbstractChat.Meta):
        verbose_name = 'group-chat'

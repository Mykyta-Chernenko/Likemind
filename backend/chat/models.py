import datetime

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models

from users.models import Person


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


class AbstartPrivateMessage(AbstractMessage):
    class Meta:
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

    class Meta:
        abstract = True


class AbstractPrivateChat(AbstractChat):
    first_user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='%(class)s_first_set')
    second_user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='%(class)s_second_set')

    class Meta:
        abstract = True

    def last_message(self):
        try:
            return self.message_set.latest('created_at')
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return f' {self.first_user} and {self.second_user}'


class PrivateChat(AbstractPrivateChat):
    pass


class EncryptedPrivateChat(AbstractPrivateChat):
    keep_time = models.DurationField(default=datetime.timedelta(minutes=1))


class GroupChat(AbstractChat):
    name = models.CharField(max_length=255)

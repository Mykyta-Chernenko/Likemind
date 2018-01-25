import datetime

from django.db import models

from users.models import Person


class AbstractMessage(models.Model):
    text = models.TextField(max_length=1000)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.TimeField(auto_created=True)
    edited = models.BooleanField(default=False)
    edited_at = models.TimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.edited_at and self.created_at and self.edited_at != self.created_at:
            self.edited = True

class Message(AbstractMessage):
    chat = models.ForeignKey('PrivateChat', on_delete=models.CASCADE)


class EnctyptedMessage(AbstractMessage):
    chat = models.ForeignKey('EncryptedPrivateChat', on_delete=models.CASCADE)

    @property
    def should_delete(self):
        return self.created_at + self.chat.keep_time < datetime.datetime.now()

class GroupMessage(AbstractMessage):
    chat = models.ForeignKey('GroupChat', on_delete=models.CASCADE)


class AbstractChat(models.Model):
    creation = models.DateTimeField(auto_created=True)
    last_use = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractPrivateChat(models.Model):
    first_user = models.ForeignKey(Person, on_delete=models.CASCADE)
    second_user = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class PrivateChat(AbstractPrivateChat):
    last_message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True, blank=True)


class EncryptedPrivateChat(AbstractPrivateChat):
    last_message = models.ForeignKey(EnctyptedMessage, on_delete=models.SET_NULL, null=True, blank=True)
    keep_time = models.DurationField(default=datetime.timedelta(minutes=1))


class GroupChat(AbstractChat):
    last_message = models.ForeignKey(GroupMessage, on_delete=models.SET_NULL, null=True, blank=True)

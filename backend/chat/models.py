import datetime

from django.db import models

from users.models import Person


class AbstractMessage(models.Model):
    text = models.TextField(max_length=1000)
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    created_at = models.TimeField(auto_now_add=True, db_index=True)
    edited = models.BooleanField(default=False)
    edited_at = models.TimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.edited_at and self.created_at and self.edited_at != self.created_at:
            self.edited = True


class PrivateMessage(AbstractMessage):
    chat = models.ForeignKey('PrivateChat', on_delete=models.CASCADE, related_name='message_set')


class EnctyptedMessage(AbstractMessage):
    chat = models.ForeignKey('EncryptedPrivateChat', on_delete=models.CASCADE, related_name='message_set')

    @property
    def should_delete(self):
        return self.created_at + self.chat.keep_time < datetime.datetime.now()


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

    @property
    def last_message(self):
        return self.message_set.latest('created_at')


class PrivateChat(AbstractPrivateChat):
    pass


class EncryptedPrivateChat(AbstractPrivateChat):
    keep_time = models.DurationField(default=datetime.timedelta(minutes=1))


class GroupChat(AbstractChat):
    name = models.CharField(max_length=255)

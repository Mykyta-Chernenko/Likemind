from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

chat_limit = models.Q(app_label='chat', model='PrivateChat') | \
             models.Q(app_label='chat', model='EncryptedPrivateChat') | \
             models.Q(app_label='chat', model='GroupChat')


class _ChatFile(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=chat_limit)
    object_id = models.PositiveIntegerField()
    chat = GenericForeignKey()

    class Meta:
        abstract = True


class ChatImage(_ChatFile):
    image = models.ImageField(upload_to='chat_images/%y/%m/%d')


class ChatAudio(_ChatFile):
    audio = models.FileField(upload_to='chat_audios/%y/%m/%d')


class ChatVideo(_ChatFile):
    video = models.FileField(upload_to='chat_videos/%y/%m/%d')


class ChatFile(_ChatFile):
    file = models.FileField(upload_to='chat_files/%y/%m/%d')

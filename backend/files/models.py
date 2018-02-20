from audiofield.fields import AudioField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from backend import settings
from users.models import Person

chat_limit = models.Q(app_label='chat', model='PrivateChat') | \
             models.Q(app_label='chat', model='EncryptedPrivateChat') | \
             models.Q(app_label='chat', model='GroupChat')


class _ChatFile(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=chat_limit)
    object_id = models.PositiveIntegerField()
    chat = GenericForeignKey()
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class ChatFile(_ChatFile):
    file = models.FileField(upload_to='chat_files/%y/%m/%d')


class ChatImage(_ChatFile):
    image = models.ImageField(upload_to='chat_images/%y/%m/%d')


class ChatAudio(_ChatFile):
    audio = AudioField(upload_to='chat_audios/%y/%m/%d', ext_whitelist=(".mp3", ".wav", ".ogg"),
                             help_text=("Allowed type - .mp3, .wav, .ogg"))

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio:
            file_url = settings.MEDIA_URL + str(self.audio)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (
                file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')




class ChatVideo(_ChatFile):
    video = models.FileField(upload_to='chat_videos/%y/%m/%d')

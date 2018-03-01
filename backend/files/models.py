from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models

from backend import settings

from users.models import Person
from utils.models_methods import _string_type

chat_limit = models.Q(app_label='chat', model='PrivateChat') | \
             models.Q(app_label='chat', model='EncryptedPrivateChat') | \
             models.Q(app_label='chat', model='GroupChat')


class _ChatFile(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=chat_limit)
    object_id = models.PositiveIntegerField()
    chat = GenericForeignKey()
    owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    @classmethod
    def get_action_class(cls):
        raise NotImplementedError

    @classmethod
    def get_serializer_class(cls):
        raise NotImplementedError('override get_serializer_class')

    @classmethod
    def string_type(cls):
        return _string_type(cls)


class ChatFile(_ChatFile):
    file = models.FileField(upload_to='chat_files/%y/%m/%d')

    @classmethod
    def get_action_class(cls):
        from utils.websocket_utils import ChatFileMessageAction
        return ChatFileMessageAction

    @classmethod
    def get_field(cls):
        return cls.file.field.name

    @classmethod
    def get_serializer_class(cls):
        from files.serializers import ChatFileSerializer
        return ChatFileSerializer


class ChatImage(_ChatFile):
    image = models.ImageField(upload_to='chat_images/%y/%m/%d')

    @classmethod
    def get_action_class(cls):
        from utils.websocket_utils import ChatImageMessageAction
        return ChatImageMessageAction

    @classmethod
    def get_field(cls):
        return cls.image.field.name

    @classmethod
    def get_serializer_class(cls):
        from files.serializers import ChatImageSerializer
        return ChatImageSerializer


class ChatAudio(_ChatFile):
    audio = models.FileField(upload_to='chat_audios/%y/%m/%d',
                             help_text=("Allowed type - .mp3, .wav, .ogg"),
                             validators=[RegexValidator(regex=r'(\.mp3|\.wav|\.ogg)$')])

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio:
            file_url = settings.MEDIA_URL + str(self.audio)
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (
                file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')

    @classmethod
    def get_action_class(cls):
        from utils.websocket_utils import ChatAudioMessageAction
        return ChatAudioMessageAction

    @classmethod
    def get_field(cls):
        return cls.audio.field.name

    @classmethod
    def get_serializer_class(cls):
        from files.serializers import ChatAudioSerializer
        return ChatAudioSerializer


class ChatVideo(_ChatFile):
    video = models.FileField(upload_to='chat_videos/%y/%m/%d',
                             help_text=("Allowed type - .avi, .flv, .mwv, .mov, .mp4"),
                             validators=[RegexValidator(regex=r'(\.avi|\.flv|\.mwv|\.mov|\.mp4)$')])

    def video_file_player(self):
        """audio player tag for admin"""
        if self.video:
            file_url = settings.MEDIA_URL + str(self.video)
            player_string = '<video src="%s" controls>Your browser does not support the audio element.</video>' % (
                file_url)
            return player_string

    @classmethod
    def get_action_class(cls):
        from utils.websocket_utils import ChatVideoMessageAction
        return ChatVideoMessageAction

    @classmethod
    def get_field(cls):
        return cls.video.field.name

    @classmethod
    def get_serializer_class(cls):
        from files.serializers import ChatVideoSerializer
        return ChatVideoSerializer

from django.contrib import admin
from django.contrib.contenttypes.admin  import GenericTabularInline

from chat.models import PrivateChat
from files.models import ChatFile, ChatAudio, ChatImage, ChatVideo


class _ChatFileInline(GenericTabularInline):
    pass
class ChatFileInline(_ChatFileInline):
    model = ChatFile
class ChatImageInline(_ChatFileInline):
    model = ChatImage
class ChatAudioInline(_ChatFileInline):
    model = ChatAudio
class ChatVideoInline(_ChatFileInline):
    model = ChatVideo

class _ChatFileAdmin(admin.ModelAdmin):
    exclude = []


@admin.register(ChatFile)
class ChatFileAdmin(_ChatFileAdmin):
    # fields = _ChatFileAdmin.fields + ['file']
    inlines = [ChatFileInline]

@admin.register(ChatAudio)
class ChatAudioAdmin(_ChatFileAdmin):
    # fields = _ChatFileAdmin.fields + ['audio']
    inlines = [ChatAudioInline]

@admin.register(ChatImage)
class ChatImageAdmin(_ChatFileAdmin):
    # fields = _ChatFileAdmin.fields + ['image']
    inlines = [ChatImageInline]

@admin.register(ChatVideo)
class ChatVideoAdmin(_ChatFileAdmin):
    # fields = _ChatFileAdmin.fields + ['video']
    inlines = [ChatVideoInline]
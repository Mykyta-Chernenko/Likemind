from django.contrib import admin

from chat.models import PrivateMessage, EncryptedPrivateMessage, GroupMessage, PrivateChat, EncryptedPrivateChat, \
    GroupChat


@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    fields = ['chat', 'owner', 'edited', 'text']


@admin.register(EncryptedPrivateMessage)
class EncryptedPrivateMessageAdmin(admin.ModelAdmin):
    fields = ['chat', 'owner', 'edited']


@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    fields = ['chat', 'owner', 'edited']


@admin.register(PrivateChat)
class PrivateChatAdmin(admin.ModelAdmin):
    fields = ['first_user', 'second_user', ]


@admin.register(EncryptedPrivateChat)
class EncryptedPrivateChatAdmin(admin.ModelAdmin):
    fields = ['first_user', 'second_user']


@admin.register(GroupChat)
class GroupChatAdmin(admin.ModelAdmin):
    fields = ['last_message']

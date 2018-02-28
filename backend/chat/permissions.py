from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from chat.consts import MESSAGE_TYPE_TO_CHAT_TYPE


class MessageBelongToChatAndUserIsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

    def has_permission(self, request, view):
        chat_model = MESSAGE_TYPE_TO_CHAT_TYPE[view.serializer_class.Meta.model]
        chat = get_object_or_404(chat_model, pk=view.kwargs['chat_id'])
        return request.user in chat.get_users()

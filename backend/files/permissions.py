from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission

from chat.consts import MESSAGE_TYPE_TO_CHAT_TYPE


class BelongToChat(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.chat.get_users()


class FileBelongToChat(BelongToChat):
    def has_permission(self, request, view):
        model = view.kwargs.get('chat_model')
        model_id = view.kwargs.get('chat_id')

        chat = get_object_or_404(model, pk=model_id)
        return request.user in chat.get_users()




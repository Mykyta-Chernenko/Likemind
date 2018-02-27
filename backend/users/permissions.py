from rest_framework.permissions import BasePermission


class BelongToFriendship(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.fist == request.user or obj.second == request.user
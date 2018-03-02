from rest_framework.permissions import BasePermission


class BelongToFriendship(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.first_user == request.user or obj.second_user == request.user
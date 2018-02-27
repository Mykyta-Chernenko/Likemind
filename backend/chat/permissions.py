from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission


class AllowMessageToOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user



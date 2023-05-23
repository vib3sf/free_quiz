from rest_framework import permissions

from polls.models import Vote


class IsPollCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Vote):
            obj = obj.choice.question.poll
        return obj.creator == request.user

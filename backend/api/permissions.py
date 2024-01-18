from django.db.models import Q
from rest_framework import permissions

from chats.models import Chat


class IsAdmin(permissions.BasePermission):
    """Права доступа для администратора."""

    def has_permission(self, request, view):
        return request.user.is_superuser


class UserCustomPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'create']:
            return request.user.is_authenticated
        else:
            return request.user.is_superuser


class IsInitiatorOrReceiverChatPermission(permissions.BasePermission):
    """
    Права для работы с чатами.

    """

    def has_permission(self, request, view):
        if view.action == 'retrieve':
            chat_id = view.kwargs['pk']
            chat = Chat.objects.get(pk=chat_id)
            return (request.user in (chat.initiator, chat.receiver))
        if view.action == 'list':
            user = request.user
            return Chat.objects.filter(
                Q(initiator=user) | Q(receiver=user)
            ).exists()
        if request.method == 'POST':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return request.user in (obj.initiator, obj.receiver)

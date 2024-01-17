from rest_framework import permissions


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

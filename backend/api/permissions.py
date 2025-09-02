# ver1
from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_staff

# from rest_framework import permissions


# class IsAdminUserOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
#     """ Класс доступа. Админ или только чтение. """

#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated
#                 and request.user.is_active
#                 and request.user.is_staff)


# class IsOwnerOrIsAdminOrReadOnly(permissions.IsAuthenticatedOrReadOnly):
#     """ Класс доступа. Админ, автор или только чтение. """

#     def has_object_permission(self, request, view, obj):
#         return (request.method in permissions.SAFE_METHODS
#                 or request.user.is_authenticated
#                 and request.user.is_active
#                 and obj.author == request.user
#                 or request.user.is_staff)

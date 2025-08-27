from rest_framework import permissions

class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение: полный доступ автору и администраторам, 
    остальным - только чтение.
    """

    def has_permission(self, request, view):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Запись разрешена только автору объекта или администратору
        return obj.author == request.user or request.user.is_staff

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied


class HasPermission(BasePermission):
    """
    Проверяет, есть ли у пользователя указанное разрешение.
    Пример использования: @permission_classes([HasPermission('user.read')])
    """
    
    def __init__(self, permission_codename):
        self.permission_codename = permission_codename
    
    def has_permission(self, request, view):
        # 1. Проверяем аутентификацию
        if not request.user.is_authenticated:
            raise AuthenticationFailed(
                detail="Требуется авторизация",
                code=401
            )
        
        # 2. Проверяем активен ли пользователь
        if not request.user.is_active:
            raise AuthenticationFailed(
                detail="Аккаунт деактивирован",
                code=401
            )
        
        # 3. Если у пользователя нет роли - доступ запрещён
        if not request.user.role:
            raise PermissionDenied(
                detail="У пользователя не назначена роль",
                code=403
            )
        
        # 4. Получаем все разрешения роли пользователя
        user_permissions = request.user.role.role_permissions.values_list(
            'permission__codename', flat=True
        )
        
        # 5. Проверяем, есть ли нужное разрешение
        if self.permission_codename in user_permissions:
            return True
        
        # 6. Если разрешения нет - доступ запрещён
        raise PermissionDenied(
            detail=f"Требуется разрешение: {self.permission_codename}",
            code=403
        )
    
    def __call__(self):
        """Позволяет использовать класс как вызываемый объект"""
        return self
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from utils.permissions import HasPermission
from .models import Role, Permission, RolePermission
from users.models import User
from .serializers import (
    RoleSerializer,
    RoleDetailSerializer,
    UserRoleSerializer,
    AddPermissionToRoleSerializer,
    PermissionSerializer
)


@api_view(['GET'])
@permission_classes([HasPermission('permission.manage')])
def role_list(request):
    """
    Получить список всех ролей
    Требуется: permission.manage
    """
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([HasPermission('permission.manage')])
def role_detail(request, pk):
    """
    Получить детали роли с разрешениями
    Требуется: permission.manage
    """
    role = get_object_or_404(Role, pk=pk)
    serializer = RoleDetailSerializer(role)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([HasPermission('permission.manage')])
def permission_list(request):
    """
    Получить список всех разрешений
    Требуется: permission.manage
    """
    permissions = Permission.objects.all()
    serializer = PermissionSerializer(permissions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([HasPermission('permission.manage')])
def add_permission_to_role(request, pk):
    """
    Добавить разрешение роли
    Требуется: permission.manage
    """
    role = get_object_or_404(Role, pk=pk)
    
    serializer = AddPermissionToRoleSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    permission_id = serializer.validated_data['permission_id']
    permission = get_object_or_404(Permission, pk=permission_id)
    
    # Проверяем, не добавлено ли уже это разрешение
    if RolePermission.objects.filter(role=role, permission=permission).exists():
        return Response(
            {"detail": "Это разрешение уже назначено данной роли"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Создаём связь
    role_permission = RolePermission.objects.create(
        role=role,
        permission=permission
    )
    
    return Response({
        "message": f"Разрешение '{permission.codename}' добавлено роли '{role.name}'",
        "role_permission_id": role_permission.id
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([HasPermission('permission.manage')])
def remove_permission_from_role(request, pk, permission_pk):
    """
    Удалить разрешение у роли
    Требуется: permission.manage
    """
    role = get_object_or_404(Role, pk=pk)
    permission = get_object_or_404(Permission, pk=permission_pk)
    
    # Ищем связь
    role_permission = get_object_or_404(
        RolePermission, 
        role=role, 
        permission=permission
    )
    
    role_permission.delete()
    
    return Response({
        "message": f"Разрешение '{permission.codename}' удалено у роли '{role.name}'"
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([HasPermission('permission.manage')])
def update_user_role(request, pk):
    """
    Изменить роль пользователя
    Требуется: permission.manage
    """
    user = get_object_or_404(User, pk=pk)
    
    serializer = UserRoleSerializer(user, data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    serializer.save()
    
    return Response({
        "message": f"Роль пользователя {user.email} обновлена",
        "user": serializer.data
    }, status=status.HTTP_200_OK)
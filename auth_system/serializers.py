from rest_framework import serializers
from .models import Role, Permission, RolePermission
from users.models import User


class PermissionSerializer(serializers.ModelSerializer):
    """Сериализатор для разрешений"""
    class Meta:
        model = Permission
        fields = ('id', 'codename', 'resource', 'action', 'description')
        read_only_fields = ('id',)


class RolePermissionSerializer(serializers.ModelSerializer):
    """Сериализатор для связи роли и разрешения"""
    permission = PermissionSerializer(read_only=True)
    permission_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = RolePermission
        fields = ('id', 'permission', 'permission_id', 'created_at')
        read_only_fields = ('id', 'created_at')


class RoleDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для роли с детальной информацией"""
    permissions = RolePermissionSerializer(
        source='role_permissions', 
        many=True, 
        read_only=True
    )
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ('id', 'name', 'description', 'permissions', 'user_count', 
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def get_user_count(self, obj):
        """Количество пользователей с этой ролью"""
        return obj.users.count()


class RoleSerializer(serializers.ModelSerializer):
    """Сериализатор для роли (без деталей)"""
    class Meta:
        model = Role
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class UserRoleSerializer(serializers.ModelSerializer):
    """Сериализатор для изменения роли пользователя"""
    role_id = serializers.IntegerField(required=True)
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'role_id', 'role_name')
        read_only_fields = ('id', 'email', 'full_name', 'role_name')
    
    def update(self, instance, validated_data):
        """Обновление роли пользователя"""
        role_id = validated_data.get('role_id')
        
        try:
            role = Role.objects.get(id=role_id)
            instance.role = role
            instance.save()
        except Role.DoesNotExist:
            raise serializers.ValidationError(
                {"role_id": "Роль с указанным ID не существует"}
            )
        
        return instance


class AddPermissionToRoleSerializer(serializers.Serializer):
    """Сериализатор для добавления разрешения роли"""
    permission_id = serializers.IntegerField(required=True)
    
    def validate(self, attrs):
        permission_id = attrs.get('permission_id')
        
        # Проверяем существование разрешения
        try:
            Permission.objects.get(id=permission_id)
        except Permission.DoesNotExist:
            raise serializers.ValidationError(
                {"permission_id": "Разрешение с указанным ID не существует"}
            )
        
        return attrs
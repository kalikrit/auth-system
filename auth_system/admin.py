from django.contrib import admin
from .models import Role, Permission, RolePermission


class PermissionInline(admin.TabularInline):
    """Разрешения прямо в роли"""
    model = RolePermission
    extra = 1  # количество пустых форм


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_count', 'permission_count', 'created_at')
    search_fields = ('name', 'description')
    inlines = [PermissionInline]
    
    def user_count(self, obj):
        return obj.users.count()
    user_count.short_description = 'Кол-во пользователей'
    
    def permission_count(self, obj):
        return obj.permissions.count()
    permission_count.short_description = 'Кол-во разрешений'


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('codename', 'resource', 'action', 'description', 'role_count', 'created_at')
    list_filter = ('resource', 'action')
    search_fields = ('codename', 'description')
    
    def role_count(self, obj):
        return obj.roles.count()
    role_count.short_description = 'Назначено ролям'


@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission', 'created_at')
    list_filter = ('role', 'permission__resource')
    search_fields = ('role__name', 'permission__codename')
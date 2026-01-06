from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Настройка отображения модели User в админке
class CustomUserAdmin(UserAdmin):
    # Поля при просмотре списка пользователей
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    
    # Поля при просмотре конкретного пользователя
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'patronymic')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Поля при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'patronymic', 'password1', 'password2'),
        }),
    )
    
    # Поиск и фильтрация
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


# Регистрируем нашу модель
admin.site.register(User, CustomUserAdmin)
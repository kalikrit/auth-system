from django.urls import path
from . import views

urlpatterns = [
    # Роли
    path('roles/', views.role_list, name='admin-role-list'),
    path('roles/<int:pk>/', views.role_detail, name='admin-role-detail'),
    
    # Разрешения
    path('permissions/', views.permission_list, name='admin-permission-list'),
    
    # Управление разрешениями ролей
    path('roles/<int:pk>/permissions/', views.add_permission_to_role, name='add-permission-to-role'),
    path('roles/<int:pk>/permissions/<int:permission_pk>/', views.remove_permission_from_role, name='remove-permission-from-role'),
    
    # Управление ролями пользователей
    path('users/<int:pk>/role/', views.update_user_role, name='update-user-role'),
]
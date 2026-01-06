from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login, logout

from .serializers import (
    RegisterSerializer, 
    LoginSerializer, 
    UserProfileSerializer,
    UserUpdateSerializer
)
from utils.permissions import HasPermission 

@api_view(['GET'])
@permission_classes([HasPermission('user.read')])
def profile_view(request):
    """Получить профиль текущего пользователя (требуется user.read)"""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
def register_view(request):
    """
    Регистрация нового пользователя
    Пример запроса:
    POST /api/register/
    {
        "email": "test@example.com",
        "password": "StrongPass123",
        "password2": "StrongPass123",
        "first_name": "Иван",
        "last_name": "Иванов",
        "patronymic": "Иванович"
    }
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()  # сохраняем пользователя
        return Response(
            {
                "message": "Пользователь успешно зарегистрирован",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.get_full_name()
                }
            },
            status=status.HTTP_201_CREATED
        )
    
    # Если данные невалидные, возвращаем ошибки
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
def login_view(request):
    """
    GET: показать форму входа
    POST: выполнить вход
    
    Вход в систему
    Пример запроса:
    POST /api/login/
    {
        "email": "test@example.com",
        "password": "StrongPass123"
    }
    """
    if request.method == 'GET':
        return Response({
            "description": "Эндпоинт для входа в систему",
            "method": "POST",
            "required_fields": {
                "email": "string",
                "password": "string"
            },
            "example": {
                "email": "user@example.com",
                "password": "your_password"
            }
        })
    # Если пользователь уже авторизован
    if request.user.is_authenticated:
        return Response(
            {"detail": "Вы уже авторизованы"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # СОЗДАЁМ СЕССИЮ - это и есть "логин" в Django
        login(request, user)
        
        return Response({
            "message": "Вход выполнен успешно",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.get_full_name(),
                "is_active": user.is_active
            }
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_view(request):
    """
    Выход из системы
    """
    if request.user.is_authenticated:
        # УДАЛЯЕМ СЕССИЮ - это и есть "логаут" в Django
        logout(request)
        return Response({"message": "Выход выполнен успешно"})
    
    return Response(
        {"detail": "Вы не авторизованы"},
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """Обновить профиль пользователя"""
    serializer = UserUpdateSerializer(
        request.user, 
        data=request.data, 
        partial=True  # разрешаем частичное обновление (для PATCH)
    )
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Профиль обновлён",
            "user": UserProfileSerializer(request.user).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account_view(request):
    """Мягкое удаление аккаунта"""
    user = request.user
    
    # 1. Помечаем как неактивного
    user.is_active = False
    user.save()
    
    # 2. Выходим из системы
    logout(request)
    
    # 3. Возвращаем ответ
    return Response({
        "message": "Аккаунт успешно деактивирован. Вы вышли из системы.",
        "note": "Ваши данные сохранены, но вы не можете войти снова."
    })
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer  # импортируем наш сериализатор


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
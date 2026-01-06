from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from utils.permissions import HasPermission
from django.views.decorators.csrf import csrf_exempt


# Моковые данные "статей"
MOCK_ARTICLES = [
    {
        "id": 1,
        "title": "Как работает Django",
        "content": "Django - это фреймворк для веб-приложений...",
        "author": "Иван Иванов",
        "created_at": "2024-01-15",
        "updated_at": "2024-01-20"
    },
    {
        "id": 2,
        "title": "Python для начинающих",
        "content": "Python - простой и мощный язык...",
        "author": "Мария Петрова",
        "created_at": "2024-01-10",
        "updated_at": "2024-01-12"
    },
    {
        "id": 3,
        "title": "REST API лучшие практики",
        "content": "Создавая REST API, следуйте этим правилам...",
        "author": "Алексей Сидоров",
        "created_at": "2024-01-05",
        "updated_at": "2024-01-08"
    }
]


@api_view(['GET'])
@permission_classes([HasPermission('article.read')])
def article_list(request):
    """
    Получить список статей
    Требуется разрешение: article.read
    """
    return Response({
        "count": len(MOCK_ARTICLES),
        "articles": MOCK_ARTICLES
    })


@csrf_exempt
@api_view(['POST'])
@permission_classes([HasPermission('article.create')])
def article_create(request):
    """
    Создать новую статью
    Требуется разрешение: article.create
    """
    data = request.data
    
    # Валидация (упрощённая)
    if not data.get('title') or not data.get('content'):
        return Response(
            {"error": "Заголовок и содержание обязательны"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Создаём "новую" статью (фейково)
    new_article = {
        "id": len(MOCK_ARTICLES) + 1,
        "title": data.get('title'),
        "content": data.get('content'),
        "author": request.user.get_full_name() or "Аноним",
        "created_at": "2024-01-20",
        "updated_at": "2024-01-20"
    }
    
    return Response({
        "message": "Статья создана (в демо-режиме данные не сохраняются)",
        "article": new_article
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([HasPermission('article.read')])
def article_detail(request, pk):
    """
    Получить детали статьи
    Требуется разрешение: article.read
    """
    try:
        article = next(a for a in MOCK_ARTICLES if a['id'] == int(pk))
        return Response(article)
    except StopIteration:
        return Response(
            {"error": "Статья не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )

@csrf_exempt
@api_view(['PUT', 'PATCH'])
@permission_classes([HasPermission('article.update')])
def article_update(request, pk):
    """
    Обновить статью
    Требуется разрешение: article.update
    """
    try:
        article = next(a for a in MOCK_ARTICLES if a['id'] == int(pk))
        
        # "Обновляем" статью (фейково)
        updated_article = article.copy()
        if 'title' in request.data:
            updated_article['title'] = request.data['title']
        if 'content' in request.data:
            updated_article['content'] = request.data['content']
        updated_article['updated_at'] = "2024-01-20"
        
        return Response({
            "message": "Статья обновлена (в демо-режиме данные не сохраняются)",
            "article": updated_article
        })
    except StopIteration:
        return Response(
            {"error": "Статья не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )

@csrf_exempt
@api_view(['DELETE'])
@permission_classes([HasPermission('article.delete')])
def article_delete(request, pk):
    """
    Удалить статью
    Требуется разрешение: article.delete
    """
    try:
        article = next(a for a in MOCK_ARTICLES if a['id'] == int(pk))
        
        return Response({
            "message": f"Статья '{article['title']}' удалена (в демо-режиме данные не удаляются)",
            "article_id": pk
        })
    except StopIteration:
        return Response(
            {"error": "Статья не найдена"},
            status=status.HTTP_404_NOT_FOUND
        )
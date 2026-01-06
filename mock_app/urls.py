from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article-list'),
    path('articles/create/', views.article_create, name='article-create'),
    path('articles/<int:pk>/', views.article_detail, name='article-detail'),
    path('articles/<int:pk>/update/', views.article_update, name='article-update'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article-delete'),
]
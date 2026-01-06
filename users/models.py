from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Менеджер пользователей - отвечает за создание пользователей
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Создаёт и возвращает пользователя с email и паролем
        """
        if not email:
            raise ValueError('Email обязателен')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Хэширует пароль
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создаёт и возвращает суперпользователя
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, password, **extra_fields)


# Сама модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    """
    Кастомная модель пользователя
    """
    email = models.EmailField('Email', unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    patronymic = models.CharField('Отчество', max_length=150, blank=True)
    
    # Статусы
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Персонал', default=False)  # доступ в админку
    
    # Даты
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)
    updated_at = models.DateTimeField('Обновлён', auto_now=True)
    
    # Связь с ролью (пока оставим, добавим позже когда создадим модель Role)
    # role = models.ForeignKey('auth_system.Role', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Менеджер объектов
    objects = CustomUserManager()
    
    # Поле для аутентификации (вместо username используем email)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']  # при создании суперпользователя
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Возвращает полное имя
        """
        return f'{self.last_name} {self.first_name} {self.patronymic}'.strip()
    
    def soft_delete(self):
        """
        Мягкое удаление пользователя
        """
        self.is_active = False
        self.save()
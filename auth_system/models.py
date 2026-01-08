from django.db import models


class Role(models.Model):
    """
    Роль пользователя (Администратор, Пользователь, Модератор и т.д.)
    """
    name = models.CharField(
        'Название роли',
        max_length=100,
        unique=True
    )
    description = models.TextField(
        'Описание роли',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        'Дата обновления',
        auto_now=True,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class Permission(models.Model):
    """
    Разрешение на действие (статья:читать, статья:писать и т.д.)
    """
    ACTION_CHOICES = [
        ('create', 'Создание'),
        ('read', 'Чтение'),
        ('update', 'Обновление'),
        ('delete', 'Удаление'),
        ('publish', 'Публикация'),
        ('approve', 'Одобрение'),
    ]
    
    RESOURCE_CHOICES = [
        ('article', 'Статья'),
        ('product', 'Товар'),
        ('user', 'Пользователь'),
        ('order', 'Заказ'),
        ('category', 'Категория'),
    ]
    
    resource = models.CharField(
        'Ресурс',
        max_length=50,
        choices=RESOURCE_CHOICES
    )
    action = models.CharField(
        'Действие',
        max_length=50,
        choices=ACTION_CHOICES
    )
    codename = models.CharField(
        'Кодовое имя',
        max_length=100,
        unique=True,
        help_text='Уникальное имя разрешения (например: article.create)'
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешения'
        unique_together = [['resource', 'action']]  # комбинация ресурс+действие должна быть уникальной
        ordering = ['resource', 'action']
    
    def __str__(self):
        return f'{self.codename} ({self.get_resource_display()}:{self.get_action_display()})'
    
    def save(self, *args, **kwargs):
        # Автоматически генерируем codename если не указан
        if not self.codename:
            self.codename = f'{self.resource}.{self.action}'
        super().save(*args, **kwargs)
        
class RolePermission(models.Model):
    """
    Связь ролей и разрешений (Many-to-Many)
    """
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role_permissions',
        verbose_name='Роль'
    )
    permission = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        related_name='roles',
        verbose_name='Разрешение'
    )
    created_at = models.DateTimeField(
        'Дата назначения',
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = 'Разрешение роли'
        verbose_name_plural = 'Разрешения ролей'
        unique_together = [['role', 'permission']]  # нельзя назначить одно разрешение роли дважды
    
    def __str__(self):
        return f'{self.role.name} → {self.permission.codename}'
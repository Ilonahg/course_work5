from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Настройки отображения модели User в админке."""

    # Поля, которые будут отображаться в списке пользователей
    list_display = ('email', 'is_staff', 'is_active')

    # Поля, доступные для редактирования
    fieldsets = (
        (None, {'fields': ('email', 'password', 'telegram_id')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    # Поля для создания нового пользователя в админке
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)

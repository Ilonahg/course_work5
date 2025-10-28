"""
Главный файл маршрутов проекта Habit Tracker.

Содержит:
- Админ-панель
- Маршруты для пользователей (регистрация, JWT авторизация)
- Маршруты для привычек
- Swagger и ReDoc для документации
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# === Swagger конфигурация ===
schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="Документация для API курсового проекта Habit Tracker",
        contact=openapi.Contact(email="support@habit-tracker.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# === Основные маршруты ===
urlpatterns = [
    path("admin/", admin.site.urls),

    # Пользователи: регистрация и JWT авторизация
    path("api/users/", include("users.urls")),

    # Привычки (CRUD, публичные привычки, пагинация и т.д.)
    path("api/habits/", include("habits.urls")),

    # Swagger и ReDoc — документация API
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi  # ← вот этот импорт обязателен

# Swagger конфигурация
schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version='v1',
        description="Документация для API курсового проекта Habit Tracker",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('habits.urls')),

    # Swagger и ReDoc
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

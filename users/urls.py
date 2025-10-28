"""
Маршруты для работы с пользователями:
- регистрация,
- авторизация (JWT),
- обновление токенов.
"""

from django.urls import path
from .views import UserRegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Регистрация нового пользователя
    path("register/", UserRegisterView.as_view(), name="register"),

    # Авторизация по email и получение пары токенов (access + refresh)
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),

    # Обновление access токена с помощью refresh токена
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

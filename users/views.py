from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомный сериализатор для JWT.
    Авторизация выполняется по email, а не по username.
    """

    @classmethod
    def get_token(cls, user):
        """Добавляем в токен полезную информацию о пользователе."""
        token = super().get_token(user)
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Возвращает пару токенов (access и refresh)
    при успешной авторизации по email и паролю.
    """
    serializer_class = CustomTokenObtainPairSerializer


class UserRegisterSerializer(ModelSerializer):
    """
    Сериализатор для регистрации пользователя.
    Создаёт нового пользователя с email и паролем.
    """

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password")

    def create(self, validated_data):
        """Создание пользователя с хешированным паролем."""
        user = User.objects.create_user(**validated_data)
        return user


class UserRegisterView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации новых пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """Создаёт пользователя и возвращает сообщение об успехе."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Пользователь успешно зарегистрирован!"},
            status=status.HTTP_201_CREATED
        )

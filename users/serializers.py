from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    - Пароль скрыт от вывода (write_only)
    - Username не обязателен (генерируется автоматически из email)
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "password")
        extra_kwargs = {
            "username": {"required": False, "allow_blank": True},
        }

    def create(self, validated_data):
        """
        Создание пользователя с шифрованием пароля.
        Если username не указан — подставляется email.
        """
        username = validated_data.get("username")
        if not username:
            username = validated_data["email"]
            validated_data["username"] = username

        user = User.objects.create_user(
            email=validated_data["email"],
            username=username,
            password=validated_data["password"]
        )
        return user

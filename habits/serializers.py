from rest_framework import serializers
from datetime import timedelta
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Habit.

    Отвечает за валидацию и преобразование данных привычек между моделью
    и JSON-форматом для API.
    """

    class Meta:
        """Мета-класс, определяющий модель и поля сериализатора."""
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate_time_to_complete(self, value):
        """
        Проверяет, что время выполнения привычки не превышает 2 минуты.

        Преобразует строку формата '00:02:00' в timedelta и выполняет валидацию.
        """
        if isinstance(value, str):
            try:
                hours, minutes, seconds = map(int, value.split(":"))
                value = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except Exception:
                raise serializers.ValidationError(
                    "Неверный формат времени выполнения. Используйте формат HH:MM:SS."
                )

        if value > timedelta(minutes=2):
            raise serializers.ValidationError(
                "Время выполнения не может превышать 2 минуты."
            )
        return value

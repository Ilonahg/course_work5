from rest_framework import serializers
from datetime import timedelta
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)  # 👈 добавляем это!

    def validate_time_to_complete(self, value):
        # Преобразуем строку "00:02:00" → timedelta
        if isinstance(value, str):
            try:
                h, m, s = map(int, value.split(":"))
                value = timedelta(hours=h, minutes=m, seconds=s)
            except Exception:
                raise serializers.ValidationError("Неверный формат времени выполнения")

        if value > timedelta(minutes=2):
            raise serializers.ValidationError("Время выполнения не может превышать 2 минуты")
        return value

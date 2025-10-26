from rest_framework import serializers


def validate_habit(data):
    """
    Валидатор для модели Habit.
    Проверяет все основные бизнес-правила SkyPro.
    """

    is_pleasant = data.get("is_pleasant")
    related_habit = data.get("related_habit")
    reward = data.get("reward")
    periodicity = data.get("periodicity")

    # 1️⃣ Нельзя одновременно указывать вознаграждение и приятную привычку
    if is_pleasant and reward:
        raise serializers.ValidationError(
            "Приятная привычка не может иметь вознаграждение."
        )

    # 2️⃣ У приятной привычки не может быть связанной привычки
    if is_pleasant and related_habit:
        raise serializers.ValidationError(
            "Приятная привычка не может иметь связанную привычку."
        )

    # 3️⃣ У привычки не может быть в качестве связанной — неприятной привычки
    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError(
            "Связанная привычка должна быть приятной."
        )

    # 4️⃣ Нельзя связать привычку саму с собой
    if related_habit and data.get("id") == related_habit.id:
        raise serializers.ValidationError(
            "Привычка не может быть связана сама с собой."
        )

    # 5️⃣ Периодичность не может быть больше 7 дней
    if periodicity and periodicity > 7:
        raise serializers.ValidationError(
            "Периодичность не может превышать 7 дней."
        )

    return data

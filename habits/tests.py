from datetime import timedelta
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from habits.models import Habit

User = get_user_model()


class HabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)
        self.habit_url = reverse("habit-list")

    def test_create_habit(self):
        """Проверка создания привычки"""
        data = {
            "action": "Пить воду",
            "place": "Дом",
            "time": "08:00:00",
            "time_to_complete": "00:01:30",  # строка — сериализатор сам преобразует
            "is_pleasant": False,
            "is_public": True,
            "periodicity": "Ежедневно",
        }
        response = self.client.post(self.habit_url, data, format="json")

        if response.status_code != 201:
            print("\nОшибка при создании:", response.data)

        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertTrue(Habit.objects.exists())

    def test_get_habits_list(self):
        """Проверка получения списка привычек"""
        Habit.objects.create(
            user=self.user,
            action="Бегать",
            place="Парк",
            time="07:00:00",
            time_to_complete=timedelta(minutes=2),
        )
        response = self.client.get(self.habit_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # учёт пагинации
        results = response.data.get("results", response.data)
        self.assertGreaterEqual(len(results), 1)

    def test_update_habit(self):
        """Проверка обновления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            action="Читать книги",
            place="Дом",
            time="22:00:00",
            time_to_complete=timedelta(minutes=1),
        )
        url = reverse("habit-detail", args=[habit.id])
        data = {"action": "Читать 10 страниц"}
        response = self.client.patch(url, data, format="json")

        if response.status_code != 200:
            print("\nОшибка при обновлении:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "Читать 10 страниц")

    def test_delete_habit(self):
        """Проверка удаления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            action="Медитировать",
            place="Комната",
            time="06:00:00",
            time_to_complete=timedelta(minutes=1),
        )
        url = reverse("habit-detail", args=[habit.id])
        response = self.client.delete(url)

        if response.status_code != 204:
            print("\nОшибка при удалении:", response.data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=habit.id).exists())
def test_habit_str(self):
    """Проверка строкового представления привычки"""
    habit = Habit.objects.create(
        user=self.user,
        action="Тестовое действие",
        place="Офис",
        time="09:00:00",
        time_to_complete=timedelta(minutes=1),
    )
    self.assertEqual(str(habit), "Тестовое действие")

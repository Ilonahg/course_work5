from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    """
    Вьюсет для управления привычками.

    Реализует CRUD-операции:
    - создание, редактирование и удаление привычек текущего пользователя;
    - просмотр своих привычек;
    - просмотр публичных привычек других пользователей.
    """

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает привычки, доступные пользователю.

        Пользователь видит:
        - свои собственные привычки;
        - публичные привычки других пользователей.
        """
        return Habit.objects.filter(Q(user=self.request.user) | Q(is_public=True))

    def perform_create(self, serializer):
        """
        Присваивает текущего пользователя при создании привычки.

        Это гарантирует, что каждая привычка принадлежит пользователю,
        создавшему её.
        """
        serializer.save(user=self.request.user)

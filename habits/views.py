from rest_framework import viewsets, permissions
from django.db import models
from .models import Habit
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(models.Q(user=self.request.user) | models.Q(is_public=True))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

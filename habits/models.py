from django.db import models
from django.conf import settings
from datetime import timedelta


class Habit(models.Model):
    PERIODICITY_CHOICES = [
        ("Ежедневно", "Ежедневно"),
        ("Раз в неделю", "Раз в неделю"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits"
    )
    action = models.CharField(max_length=255)
    place = models.CharField(max_length=255, blank=True, null=True)
    time = models.TimeField()
    time_to_complete = models.DurationField(default=timedelta(minutes=2))
    is_pleasant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)
    periodicity = models.CharField(max_length=50, choices=PERIODICITY_CHOICES, default="Ежедневно")
    reward = models.CharField(max_length=255, blank=True, null=True)
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="linked_habits"
    )

    def __str__(self):
        return f"{self.action} ({self.user})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

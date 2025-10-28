from django.db import models
from django.conf import settings
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


class Habit(models.Model):
    """
    Модель привычки.

    Описывает привычку пользователя, включая действие, место, время,
    периодичность, вознаграждение и признак публичности.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь"
    )
    action = models.CharField(
        max_length=255,
        verbose_name="Действие",
        help_text="Действие, которое необходимо выполнить."
    )
    place = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Место",
        help_text="Место, где выполняется привычка."
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="Время, когда нужно выполнять привычку."
    )
    time_to_complete = models.DurationField(
        default=timedelta(minutes=2),
        verbose_name="Время на выполнение",
        help_text="Предполагаемое время на выполнение привычки (до 120 секунд)."
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Указывает, является ли привычка приятной."
    )
    is_public = models.BooleanField(
        default=True,
        verbose_name="Публичная привычка",
        help_text="Если истина, привычка видна другим пользователям."
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность (в днях)",
        help_text="Как часто выполняется привычка (от 1 до 7 дней)."
    )
    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь себя вознаградит за выполнение привычки."
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_habits",
        verbose_name="Связанная привычка",
        help_text="Приятная привычка, связанная с выполнением основной привычки."
    )

    def __str__(self):
        """Возвращает строковое представление привычки."""
        return f"{self.action} ({self.user})"

    class Meta:
        """Метаданные модели Habit."""
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

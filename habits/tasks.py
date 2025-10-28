import requests
from django.conf import settings
from celery import shared_task
from .models import Habit


@shared_task
def send_habit_reminder(habit_id):
    """
    Отправляет напоминание в Telegram о необходимости выполнить привычку.

    Аргументы:
        habit_id (int): Идентификатор привычки, для которой нужно отправить уведомление.

    Функция получает объект привычки из базы данных, формирует текст напоминания
    и отправляет его пользователю через Telegram Bot API.
    """
    print(f"📬 Задача Celery запущена для habit_id={habit_id}")

    try:
        # Получаем привычку по ID
        habit = Habit.objects.get(id=habit_id)

        # Формируем сообщение
        message = (
            f"🔔 Напоминание! Пора выполнить привычку: "
            f"{habit.action} в {habit.time.strftime('%H:%M')}."
        )
        print("📨 Сообщение для Telegram:", message)

        # Достаём токен и chat_id из переменных окружения
        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        print(f"Используем токен: {bot_token[:10]}... и chat_id: {chat_id}")

        # Отправляем сообщение пользователю
        if bot_token and chat_id:
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                data={"chat_id": chat_id, "text": message},
                timeout=10
            )
            print("📤 Ответ Telegram:", response.status_code, response.text)
        else:
            print("⚠️ Отсутствуют TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID в настройках.")

    except Habit.DoesNotExist:
        print(f"⚠️ Привычка с id={habit_id} не найдена. Напоминание не отправлено.")
    except Exception as e:
        print(f"❌ Ошибка при отправке уведомления: {e}")

import requests
from django.conf import settings
from celery import shared_task
from .models import Habit


@shared_task
def send_habit_reminder(habit_id):
    print(f"📬 Задача Celery запущена для habit_id={habit_id}")
    try:
        habit = Habit.objects.get(id=habit_id)
        message = f"🔔 Напоминание! Пора выполнить привычку: {habit.action} в {habit.time.strftime('%H:%M')}."
        print("📨 Сообщение для Telegram:", message)

        bot_token = settings.TELEGRAM_BOT_TOKEN
        chat_id = settings.TELEGRAM_CHAT_ID
        print(f"Используем токен: {bot_token[:10]}... и chat_id: {chat_id}")

        if bot_token and chat_id:
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                data={"chat_id": chat_id, "text": message},
            )
            print("📤 Ответ Telegram:", response.status_code, response.text)

    except Habit.DoesNotExist:
        print(f"⚠️ Habit {habit_id} не существует.")

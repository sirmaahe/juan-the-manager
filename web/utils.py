import requests

from .settings import TELEGRAM_BOT_KEY


def send_tg_message(chat_id, message):
    requests.post(
        f'https://api.telegram.org/bot{TELEGRAM_BOT_KEY}/sendMessage',
        json={
            "chat_id": chat_id,
            "text": message
        }
    )

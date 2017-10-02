import grequests

from .settings import tg_bot_key


async def send_tg_message(username, message):
    return grequests.post(
        f'https://api.telegram.org/bot{tg_bot_key}/sendMessage',
        json={
            "chat_id": username,
            "text": message
        }
    )

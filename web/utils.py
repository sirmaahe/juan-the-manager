import json

import aiohttp

from .settings import TELEGRAM_BOT_KEY


async def send_tg_message(chat_id, message):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f'https://api.telegram.org/bot{TELEGRAM_BOT_KEY}/sendMessage',
            data=json.dumps({"chat_id": chat_id, "text": message})
        ) as resp:
            return await resp.json()

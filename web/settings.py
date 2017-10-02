import os

TELEGRAM_SECRET_TOKEN = "qwerty12345"

db_url = os.environ.get('DATABASE_URL')

if db_url:
    from urllib.parse import urlparse

    result = urlparse(db_url)
    username = result.username

    DB_SETTINGS = {
        'provider': 'postgres',
        'user': result.username,
        'password': result.password,
        'database': result.path[1:],
        'host': result.hostname,
    }
else:
    DB_SETTINGS = {
        'provider': 'sqlite',
        'filename': '../database.sqlite',
        'create_db': True
    }

APP_SETTINGS = {
    'SANIC_JWT_USER_ID': 'id'
}

tg_bot_key = os.environ.get('TELEGRAM_BOT_KEY')
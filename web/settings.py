import os

TELEGRAM_SECRET_TOKEN = "qwerty12345"

db_url = os.environ.get('DATABASE_URL')

DB_SETTINGS = {
    'provider': 'postgres' if db_url else 'sqlite',
    'filename': db_url or'../database.sqlite'
}

import os

TELEGRAM_SECRET_TOKEN = "qwerty12345"

db_url = os.environ.get('DATABASE_URL')

if db_url:
    from urllib.parse import urlparse

    result = urlparse(db_url)
    username = result.username

    DB_SETTINGS = {
        'provider': 'postgres',
        'username': result.username,
        'password': result.password,
        'database': result.path[1:],
        'hostname': result.hostname,
    }
else:
    DB_SETTINGS = {
        'provider': 'sqlite',
        'filename': '../database.sqlite'
    }

from random import randint

from sanic import Sanic
from sanic.response import json

from pony.orm import db_session
from sanic_jwt import initialize, exceptions

from .settings import *
from .utils import send_tg_message
from .models import db, User, Note

db.bind(**DB_SETTINGS)
db.generate_mapping(create_tables=True)


async def authenticate(request):
    if not request.json:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    with db_session:
        user = User.get(username=username)

    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if not user.compare_passwords(password):
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user


app = Sanic()
initialize(app, authenticate)
app.config.update(APP_SETTINGS)

app.static('/static', './static/build/static/')
app.static('/html', './static/build/')


@app.route("/hooks/telegram/{}".format(TELEGRAM_SECRET_TOKEN), ["POST"])
async def telegram_hook(request):
    data = request.json
    message = data['message']
    username = message['from']['username']

    with db_session:
        user = User.get(username=username)
        if not user:
            chat_id = message['chat']['id']
            password = ''.join((chr(randint(33, 126)) for _ in range(16)))
            user = User(username=username, password=User.get_password(password), tg_chat=chat_id)
            send_tg_message(chat_id, f'Your password: {password}')

        Note(text=message['text'], user=user)

    return json({})


@app.route("/notes", ["GET"])
async def notes(request):
    payload = request.app.auth.extract_payload(request)
    if not payload:
        return json([])
    with db_session:
        response = [note.text for note in Note.select(lambda p: p.user.id == payload['user_id'])]
    return json(response)


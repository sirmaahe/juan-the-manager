from sanic import Sanic
from sanic.response import json
from pony.orm import db_session
from sanic_jwt import initialize, exceptions

from .settings import *
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
            user = User(username=username, password=message)

        Note(text=message['text'], user=user)

    return json({})


@app.route("/notes", ["GET"])
async def notes(request):
    payload = request.app.auth.extract_payload(request)
    with db_session:
        response = [note.text for note in Note.select(lambda p: p.user.id == payload['user_id'])]
    return json(response)


from sanic import Sanic
from sanic.response import json
from pony.orm import db_session

from .settings import *
from .models import db, User, Note

db.bind(**DB_SETTINGS, create_db=True)
db.generate_mapping(create_tables=True)

app = Sanic()


@app.route("/hooks/telegram/{}".format(TELEGRAM_SECRET_TOKEN), ["POST"])
async def telegram_hook(request):
    data = request.json
    message = data['message']
    username = message['from']['username']

    with db_session:
        user = User.get(username=username)
        if not user:
            user = User(username=username, password='0')

        Note(text=message['text'], user=user)

    return json({})


@app.route("/", ["GET"])
async def index(request):
    with db_session:
        users = User.all()
        response = [{"username": user.username, "notes": [note.text for note in user.notes]} for user in users]

    return json(response)


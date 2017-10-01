from sanic import Sanic
from sanic.response import json
from pony.orm import db_session

from .settings import *
from .models import db, User, Note

db.bind(**DB_SETTINGS)
db.generate_mapping(create_tables=True)

app = Sanic()

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
            user = User(username=username, password='0')

        Note(text=message['text'], user=user)

    return json({})


@app.route("/notes", ["GET"])
async def notes(request):
    with db_session:
        user = User.get(id=1)
        response = [note.text for note in user.notes]
    return json(response)


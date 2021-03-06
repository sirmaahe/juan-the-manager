from random import randint

from sanic import Sanic
from sanic.response import json, HTTPResponse

from pony.orm import db_session
from sanic_jwt import initialize, exceptions
from sanic_restplus import fields, Api, Resource

from .settings import *
from .utils import send_tg_message
from .models import db, User, Note, Category

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


api = Api(app)

notes_namespace = api.namespace('notes')
@db_session
def f(x):
    b = x.category.name if hasattr(x, 'category') else None
    return b
note_model = api.model('Note', {
    'id': fields.Integer(readOnly=True, description='id'),
    'text': fields.String(required=True, description='text'),
    'category': fields.String(attribute=f),
})

category_model = api.model('Category', {
    'id': fields.Integer(readOnly=True, description='id'),
    'name': fields.String(required=True, description='name'),
})


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
            await send_tg_message(chat_id, f'Your password: {password}')

        Note(text=message['text'], user=user)

    return json({})


@notes_namespace.route("/")
class NotesList(Resource):
    @api.marshal_with(note_model)
    async def get(self, request):
        payload = request.app.auth.extract_payload(request)
        if not payload:
            return []
        with db_session:
            response = [note for note in Note.select(lambda p: p.user.id == payload['user_id'])]
        return response


@notes_namespace.route("/<id:int>/")
class NotesList(Resource):
    async def delete(self, request, id):
        payload = request.app.auth.extract_payload(request)
        with db_session:
            Note.select(lambda n: n.user.id == payload['user_id'] and n.id == id).delete(bulk=True)
        return HTTPResponse(status=204)


@notes_namespace.route("/<id:int>/category/")
class CategoryDetail(Resource):
    @api.marshal_with(category_model)
    async def get(self, request, id):
        payload = request.app.auth.extract_payload(request)
        with db_session:
            category = Note.select(lambda n: n.user.id == payload['user_id'] and n.id == id)[0].category
        return category

    async def post(self, request, id):
        payload = request.app.auth.extract_payload(request)
        data = request.json
        name = data['name']
        with db_session:
            note = list(Note.select(lambda n: n.user.id == payload['user_id'] and n.id == id))[0]
            category = note.category
            if not category:
                Category(name=name, notes=note)
        return HTTPResponse(status=201)


app.router.add("/hooks/telegram/{}".format(TELEGRAM_SECRET_TOKEN), ["POST"], telegram_hook)

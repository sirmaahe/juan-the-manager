from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/", ["POST"])
async def telegram_hook(request):
    print(request.json)
    return json({"hello": "world"})

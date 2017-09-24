from sanic import Sanic
from sanic.response import json

app = Sanic()


@app.route("/", "POST")
async def test(request):
    print(request.json)
    return json({"hello": "world"})

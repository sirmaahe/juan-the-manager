from aiohttp import web


async def index(request):
    print(await request.json())
    return web.Response(text="Hello, world")

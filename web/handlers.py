from aiohttp import web


async def index(request):
    print(request)
    return web.Response(text="Hello, world")

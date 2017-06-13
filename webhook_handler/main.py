from aiohttp import web


async def process_message(request):
    return web.Response(text="Hello, world")

app = web.Application()
app.router.add_get('/', process_message)

web.run_app(app)

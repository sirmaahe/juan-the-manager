from aiohttp import web

from web.router import routes


def configure_handlers(app, routing_map, prefix=None):
    for routing in routing_map:
        path = prefix + routing.path if prefix is not None else routing.path
        app.router.add_route(routing.method, path, routing.handler, name=routing.name)


main = web.Application()
configure_handlers(main, routes)

from collections import namedtuple

from web.handlers import index


Route = namedtuple('Route', ['name', 'method', 'path', 'handler'])

routes = [
    Route('index', 'GET', '/', index),
]

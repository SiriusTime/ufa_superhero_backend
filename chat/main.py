#  import aiohttp_cors

import asyncio

from aiohttp import web

from views import connect
#  from views import routes


class Main:

    def _run(self):
        loop = asyncio.get_event_loop()

        app = web.Application(loop=loop)
        app['channels'] = []  # TODO change to DB
        app['users'] = {}

        app.add_routes([
            web.get('/api/chat/connect/', connect)
        ])

        web.run_app(app, port=2304)


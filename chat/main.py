#  import aiohttp_cors

import asyncio

from aiohttp import web

from views import echo
#  from views import routes


class Main:

    def _run(self):
        loop = asyncio.get_event_loop()

        app = web.Application(loop=loop)
        app['channels'] = {}  # TODO change to DB

        app.add_routes([
            web.get('/api/chat/echo/', echo),
        ])

        web.run_app(app)

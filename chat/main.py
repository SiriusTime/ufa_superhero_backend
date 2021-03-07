#  import aiohttp_cors

import asyncio

from aiohttp import web

from views import websocket_echo
#  from views import routes


class MainMixin:

    def get_routes(self):
        return [
            web.get('/api/echo/', websocket_echo),
        ]

    def create_app(self):
        loop = asyncio.get_event_loop()

        app = web.Application(loop=loop)
        app['channels'] = {}  # TODO change to DB

        app.add_routes(self.get_routes())

        app = web.Application(loop=loop)
        return app

    def _run(self):
        """
            app.router.add_routes(routes)
            cors = aiohttp_cors.setup(app, defaults={
                "*": aiohttp_cors.ResourceOptions(
                        allow_credentials=True,
                        expose_headers="*",
                        allow_headers="*",
                    )
            })
    
            for route in list(app.router.routes()):
                cors.add(route)
        """  # TODO add later

        web.run_app(app)

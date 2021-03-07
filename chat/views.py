from aiohttp import web
from aiohttp_session import get_session


class BaseLogicMixinChat:
    async def connect(self, request):
        request.session = await get_session(request)

        ws = web.WebSocketResponse()
        request.app["channels"][request.session] = ws
        await ws.prepare(request)

        return ws

    async def validate(self, request):
        for session, client in request.app['channels'].items():
            try:
                pass
            except ConnectionResetError:
                del request.app['channels'][session]

    async def send(self, request, message, session):
        peer = request.app["channels"][session]
        peer.send_json(message.as_dict())

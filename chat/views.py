from aiohttp import web
from aiohttp_session import get_session


class BaseLogicMixinChat:
    async def get_session(self, request):
        session = await get_session(request)
        return session

    async def connect(self, request):
        request.session = self.get_session(request)

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


class BaseLogicChat(BaseLogicMixinChat):
    async def send_all(self, request, message):
        for peer in request.app["channels"].values():
            await peer.send_json(message.as_dict())


async def echo(request):
    ws = BaseLogicChat().connect(request)
    await BaseLogicChat().send_all(request, "{'text': 'hello'}")
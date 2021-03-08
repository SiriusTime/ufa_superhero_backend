import json

from aiohttp import web
from aiohttp_session import get_session

from motor import motor_asyncio as ma


class BaseLogicMixinChat:
    async def get_session(self, request):
        session = await get_session(request)
        return session

    async def connect(self, request):
        request.session = self.get_session(request)

        ws = web.WebSocketResponse()
        request.app["channels"][request.session] = ws
        await ws.prepare(request)


class BaseLogicChat(BaseLogicMixinChat):
    async def send_all(self, request, message):
        for peer in request.app["channels"].values():
            await peer.send_str(message)


class DataMixinService:

    async def connect(self):
        client = ma.AsyncIOMotorClient('mongodb://localhost:27017')
        return client['users']

    async def create_collection(self, title="data", client=connect()):
        return client[title]

    async def do_insert(self, data):
        db = await self.connect()
        await db.data.insert_one(data)

    async def find(self):
        data = await self.create_collection()
        return [session for session in data]


class DataChat(DataMixinService, BaseLogicChat):

    async def validate_task(self, request):
        data = {}
        for session, client in request.app['channels'].items():
            try:
                data[session] = client
            except ConnectionResetError:
                del request.app['channels'][session]

        await self.save(data)

    async def save(self, data):
        await self.do_insert(data)

    async def update(self):
        pass


async def validate(request):
    await DataChat().validate_task(request)


async def echo(request):
    await BaseLogicChat().connect(request)
    await BaseLogicChat().send_all(request, json.dumps({"text": "hello"}))
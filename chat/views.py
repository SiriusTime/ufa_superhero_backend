import json

from aiohttp import web
from aiohttp_session import get_session

from motor import motor_asyncio as ma


class BaseLogicMixinChat:
    async def get_session(self, request):
        session = await get_session(request)
        return session

    async def send_to(self, request, data):

        await request.app["channels"][data["to"]].send_str(data["msg"])

    async def connect(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        data = await ws.receive()
        data_set = json.loads(data.data)

        request.app["channels"][data_set["user"]] = ws
        await request.app["channels"][data_set["to"]].send_str(data_set["msg"])


class DataMixinService:

    async def connect_db(self):
        client = ma.AsyncIOMotorClient('mongodb://localhost:27017')
        return client['users']

    async def create_collection(self, title="data", client=None):
        client = self.connect_db()
        return client[title]

    async def do_insert(self, data):
        db = await self.connect_db()
        await db.data.insert_one(data)

    async def find(self):
        data = await self.create_collection()
        return [session for session in data]


class DataChat(DataMixinService, BaseLogicMixinChat):

    async def validate_task(self, request):
        data = {}
        for session, client in request.app['channels'].items():
            try:
                data[session] = client
            except ConnectionResetError:
                del request.app['channels'][session]

        # await self.save(data)

    async def save(self, data):
        await self.do_insert(data)

    async def update(self):
        pass


async def validate(request):
    await DataChat().validate_task(request)  # TODO create task on asyncio


async def connect(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app['channels'].append(ws)
    async for msg in ws:
        for pk, client in enumerate(request.app['channels']):
            try:
                data = json.loads(msg.data)
                request.app["users"][data["user"]] = client
                await request.app["users"][data["to"]].send_str(data["msg"])
            except ConnectionResetError:
                try:
                    del request.app['users']["to"]
                except KeyError:
                    print("error struct msg")
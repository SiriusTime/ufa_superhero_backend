import asyncio
import json

import aiohttp


async def run():
    session = aiohttp.ClientSession()
    ws = await session.ws_connect(
        'ws://127.0.0.1:8080/api/chat/echo/')

    while True:
        data_send = {
            "user": "1",
            "to": "1",
            "msg": "Hello"
        }
        await ws.send_str(json.dumps(data_send))
        data = await ws.receive()
        print(data.data)
        print("step")
        await asyncio.sleep(5)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.Task(run()))
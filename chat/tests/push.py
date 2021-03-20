import json

from websocket import create_connection


class WebsocketService:

    def connect(self, data, port=2304):
        ws = create_connection("ws://127.0.0.1:{}/api/chat/connect/".format(port))
        message = json.dumps(data)
        print(message)
        ws.send(message)


WebsocketService().connect(
    {
        "user": "1",
        "to": "1",
        "msg": "Djo"
    }
)
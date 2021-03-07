import json

from websocket import create_connection


class WebsocketService:

    def connect(self, data, port=8080):
        ws = create_connection("ws://127.0.0.1:{}/api/chat/echo/".format(port))
        message = json.dumps(data)
        ws.send(message)


WebsocketService().connect(
    {
        "phone": "+7009",
        "email": "mail@dns1.ru",
        "first_name": "Djo",
        "password": "123456",
        "date_birthday": "1994-02-20",
        "gender": "male"
    }
)
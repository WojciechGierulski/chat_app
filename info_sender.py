import json
from datetime import datetime


class InfoSender:

    @staticmethod
    def send_json(msg, client):
        msg = json.dumps(msg)
        client.send_msg(msg)

    @staticmethod
    def message_transform(text, client):
        now = datetime.now()
        hour = now.hour if now.hour >= 10 else "0" + str(now.hour)
        minute = now.minute if now.minute >= 10 else "0" + str(now.minute)
        return {"command": "new_message", "msg": [f"{hour}:{minute}", client.name, text]}

    @staticmethod
    def disconnect(client):
        client.send_msg(json.dumps({"command": client.DISCONNECT_MSG}))

    @staticmethod
    def leave_chat_room(client):
        msg = {"command": "leave_chat_room"}
        InfoSender.send_json(msg, client)

    @staticmethod
    def send_chat_mes(client, text):
        data = InfoSender.message_transform(text, client)
        InfoSender.send_json(data, client)

    @staticmethod
    def set_name(client, name):
        data = {"command": "set_name", "name": name}
        InfoSender.send_json(data, client)

    @staticmethod
    def request_servers(client):
        data = {"command": "servers_list"}
        InfoSender.send_json(data, client)

    @staticmethod
    def create_server(client, list):
        """
        list = [server_name, password, capacity]
        """
        data = {"command": "create_server",
                "server": {"server_name": list[0], "password": list[1], "capacity": list[2]}}
        InfoSender.send_json(data, client)

    @staticmethod
    def join_server(client, server_name, password=""):
        data = {"command": "join_server", "server": {"server_name": server_name, "password": password}}
        InfoSender.send_json(data, client)

    @staticmethod
    def request_previous_messages(client):
        data = {"command": "previous_messages"}
        InfoSender.send_json(data, client)

import json
from datetime import datetime
from tkinter import messagebox


class InfoSender:

    @staticmethod
    def send_json(msg, client, handler):
        msg = json.dumps(msg)
        try:
            client.send_msg(msg)
        except:
            handler()
            messagebox.showerror("Connection Error", "Failed to send data to server")

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
    def leave_chat_room(client, handler):
        msg = {"command": "leave_chat_room"}
        InfoSender.send_json(msg, client, handler)

    @staticmethod
    def send_chat_mes(client, text, handler):
        data = InfoSender.message_transform(text, client)
        InfoSender.send_json(data, client, handler)

    @staticmethod
    def set_name(client, name, handler):
        data = {"command": "set_name", "name": name}
        InfoSender.send_json(data, client, handler)

    @staticmethod
    def request_servers(client, handler):
        data = {"command": "servers_list"}
        InfoSender.send_json(data, client, handler)

    @staticmethod
    def create_server(client, list, handler):
        """
        list = [server_name, password, capacity]
        """
        data = {"command": "create_server",
                "server": {"server_name": list[0], "password": list[1], "capacity": list[2]}}
        InfoSender.send_json(data, client, handler)

    @staticmethod
    def join_server(client, server_name, password, handler):
        data = {"command": "join_server", "server": {"server_name": server_name, "password": password}}
        InfoSender.send_json(data, client, handler)

    @staticmethod
    def request_previous_messages(client, handler):
        data = {"command": "previous_messages"}
        InfoSender.send_json(data, client, handler)

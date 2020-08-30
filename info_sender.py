import json
from datetime import datetime


class InfoSender:

    @staticmethod
    def message_transform(text, client):
        now = datetime.now()
        hour = now.hour if now.hour >= 10 else "0" + str(now.hour)
        minute = now.minute if now.minute >= 10 else "0" + str(now.minute)
        return [f"{hour}:{minute}", client.name, text]

    @staticmethod
    def disconnect(client):
        client.send_msg(client.DISCONNECT_MSG)

    @staticmethod
    def leave_chat_room(client):
        client.send_msg("leave_chat_room")

    @staticmethod
    def send_chat_mes(client, text):
        data = InfoSender.message_transform(text, client)
        data2 = json.dumps(data)
        client.send_msg("chat_message")
        client.send_msg(data2)

    @staticmethod
    def set_name(client, name):
        client.send_msg("set_name")
        client.send_msg(name)

    @staticmethod
    def request_servers(client):
        client.send_msg("servers_list")

    @staticmethod
    def create_server(client, list):
        """
        list = [server_name, password, capacity]
        """
        data = {"server_name": list[0], "password": list[1], "capacity": list[2]}
        data2 = json.dumps(data)
        client.send_msg("create_server")
        client.send_msg(data2)

    @staticmethod
    def join_server(client, server_name, password=""):
        client.send_msg("join_server")
        msg = json.dumps({"server_name": server_name, "password": password})
        client.send_msg(msg)

    @staticmethod
    def request_previous_messages(client):
        client.send_msg("previous_messages")

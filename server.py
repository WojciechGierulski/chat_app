import threading
import socket
from chat_room import ChatRoom
import json
import sys
from data_checkers import *


class User:
    def __init__(self, thread):
        self.thread = thread
        self.name = ""
        self.host = False


class Server:
    """
    users:   {conn: User}
    commands:      {command: function(conn)}
    """
    PORT = 5060
    HEADER = 16
    FORMAT = "utf-8"
    DISCONNECT_MSG = "!DISCONNECT!"
    SERVER = "0.0.0.0"
    ADDR = (SERVER, PORT)

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.commands = {}
        self.load_commands()
        self.run = False
        self.users = {}
        self.rooms = []

    def load_commands(self):
        self.commands["set_name"] = self.set_name
        self.commands["create_server"] = self.create_chat_room
        self.commands["chat_message"] = self.chat_message_handle
        self.commands["servers_list"] = self.send_servers_list
        self.commands["previous_messages"] = self.send_previous_messages
        self.commands["leave_chat_room"] = self.leave_chat_room
        self.commands["join_server"] = self.join_server

    def start(self):
        self.run = True
        self.server.listen()
        self.thread1 = threading.Thread(target=self.exit_thread, args=())
        self.thread1.start()
        while self.run:
            try:
                conn, addr = self.server.accept()
                self.users[conn] = User((threading.Thread(target=self.handle_client, args=(conn, addr))))
                self.users[conn].thread.start()
            except OSError:
                sys.exit()

    def exit_thread(self):
        runn = True
        while runn:
            x = input("type exit to stop server")
            if x == "exit":
                runn = False
                self.run = False
                self.server.close()
                for conn in self.users.keys():
                    self.send_msg("server_crashed", conn)

    def receive_msg(self, conn):
        msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            return conn.recv(int(msg_length)).decode(self.FORMAT)
        else:
            return None

    def handle_client(self, conn, addr):
        connected = True
        while connected:
            msg = self.receive_msg(conn)
            if msg == self.DISCONNECT_MSG:
                self.disconnect_client(conn)
                connected = False
            else:
                self.commands[msg](conn)
        conn.close()

    def send_msg(self, message, conn):
        msg = message.encode(self.FORMAT)
        msg_len = str(len(msg)).encode(self.FORMAT)
        msg_len += b' ' * (self.HEADER - len(msg_len))
        conn.send(msg_len)
        conn.send(msg)

    def find_room_by_user_name(self, name):
        found_room = None
        for room in self.rooms:
            if name in room.connections.keys():
                found_room = room
                break
        return found_room

    def find_room_by_name(self, name):
        found_room = None
        for room in self.rooms:
            if name == room.name:
                found_room = room
                break
        return found_room

    def get_user_names(self):
        return [user.name for user in self.users.values()]

    def get_server_names(self):
        return [room.name for room in self.rooms]

    def send_message_to_all(self, msg, room, excepts=[]):
        room.add_message(msg)
        for connection in room.connections.values():
            if connection not in excepts:
                self.send_msg("new_message", connection)
                self.send_msg(json.dumps(msg), connection)

    #######################################  COMMANDS BELOW  #############################################

    def disconnect_client(self, conn):
        self.leave_chat_room(conn)
        del self.users[conn]

    def leave_chat_room(self, conn):
        name = self.users[conn].name
        room = self.find_room_by_user_name(name)
        if room is not None:
            if room.host_name != name:
                self.send_message_to_all(f"SERVER: {name} disconnected!", room, conn)
                del room.connections[name]
            else:
                msg = "host_disconnected"
                self.send_message_to_all(msg, room, [conn])
                del room.connections[name]
                self.rooms.remove(room)

    def set_name(self, conn):
        name = self.receive_msg(conn)
        if name_checker(name, self.get_user_names()) == "ok":
            self.send_msg("name_ok", conn)
            self.users[conn].name = name
        else:
            self.send_msg("messagebox", conn)
            self.send_msg(name_checker(name, self.get_user_names()), conn)

    def create_chat_room(self, conn):
        room_properties = json.loads(self.receive_msg(conn))
        name = room_properties["server_name"]
        password = room_properties["password"]
        capacity = room_properties["capacity"]
        if name_checker(name, self.get_server_names()) == "ok":
            if password_checker(password) == "ok":
                if capacity_checker(capacity) == "ok":
                    self.send_msg("server_ok", conn)
                    self.rooms.append(ChatRoom(name, capacity, self.users[conn].name, password))
                    self.rooms[-1].connect_client(self.users[conn].name, conn)
                    self.users[conn].host = True
                else:
                    self.send_msg("messagebox", conn)
                    self.send_msg(capacity_checker(capacity), conn)
            else:
                self.send_msg("messagebox", conn)
                self.send_msg(password_checker(password), conn)
        else:
            self.send_msg("messagebox", conn)
            self.send_msg(name_checker(name, self.get_server_names()), conn)

    def chat_message_handle(self, conn):
        message = json.loads(self.receive_msg(conn))
        self.send_message_to_all(message, self.find_room_by_user_name(self.users[conn].name))

    def send_servers_list(self, conn):
        rooms = []
        for room in self.rooms:
            chat_room = {"Name": room.name, "Capacity": room.capacity, "People": len(room.connections),
                         "Password": room.password, "Host": room.host_name}
            rooms.append(chat_room)
        msg = json.dumps(rooms)
        self.send_msg("servers_list", conn)
        self.send_msg(msg, conn)

    def send_previous_messages(self, conn):
        name = self.users[conn].name
        msg = json.dumps(self.find_room_by_user_name(name).messages)
        self.send_msg("previous_messages", conn)
        self.send_msg(msg, conn)

    def join_server(self, conn):
        info = json.loads(self.receive_msg(conn))
        server_name = info["server_name"]
        password = info["password"]
        room = self.find_room_by_name(server_name)
        if room is not None:
            if room.capacity > len(room.connections):
                if password == room.password:
                    self.send_msg("join_ok", conn)
                    room.connect_client(self.users[conn].name, conn)
                    self.send_message_to_all(f"SERVER: {self.users[conn].name} joined!", room, [conn])
                else:
                    self.send_msg("messagebox", conn)
                    self.send_msg("Incorrect password", conn)
            else:
                self.send_msg("messagebox", conn)
                self.send_msg("Room is full", conn)
        else:
            self.send_msg("messagebox", conn)
            self.send_msg("Room does not exist", conn)

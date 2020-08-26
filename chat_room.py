
class ChatRoom:
    def __init__(self, name, capacity, host_name, password=""):
        self.name = name
        self.capacity = int(capacity)
        self.host_name = host_name
        self.password = password
        self.connections = {}
        self.messages = []

    def connect_client(self, name, conn):
        self.connections[name] = conn

    def add_message(self, message):
        self.messages.append(message)
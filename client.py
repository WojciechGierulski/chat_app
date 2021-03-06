import socket

class Client:
    PORT = 5060
    HEADER = 16
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    FORMAT = "utf-8"
    DISCONNECT_MSG = "!DISCONNECT!"

    def __init__(self):
        self.name = ""
        self.client = None
        self.connected = False

    def connect(self):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(self.ADDR)
            self.connected = True
        except ValueError:
            pass

    def send_msg(self, message):
        msg = message.encode(self.FORMAT)
        msg_len = str(len(msg)).encode(self.FORMAT)
        msg_len += b' ' * (self.HEADER - len(msg_len))
        self.client.send(msg_len)
        self.client.send(msg)

    def rec_msg(self):
        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
        if msg_length:
            return self.client.recv(int(msg_length)).decode(self.FORMAT)
        else:
            return None

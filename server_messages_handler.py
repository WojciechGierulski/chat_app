import threading
from tkinter import messagebox
import tkinter
import json


class Handler:
    @staticmethod
    def servers_list_convert(list):
        new_list = []
        for room in list:
            if room["Password"] == "":
                protected = "No"
            else:
                protected = "Yes"
            new_list.append(
                f"|  {room['Name']}  |  {room['People']}/{room['Capacity']}  |  Protected: {protected}  |  Host: {room['Host']}  |")
        return new_list

    def __init__(self, interface):
        self.run = True
        self.interface = interface
        self.client = self.interface.client
        self.commands = {}
        self.load_commands()
        self.thread = threading.Thread(target=self.start_handling)
        self.thread.start()

    def start_handling(self):
        while self.run:
            if self.client.connected:
                msg = self.client.rec_msg()
                if msg:
                    msg = json.loads(msg)
                    self.commands[msg["command"]](msg)

    def load_commands(self):
        self.commands["new_message"] = self.new_message
        self.commands["server_crashed"] = self.server_crashed
        self.commands["host_disconnected"] = self.host_disconnected
        self.commands["servers_list"] = self.servers_list
        self.commands["previous_messages"] = self.previous_messages
        self.commands["messagebox"] = self.messagebox
        self.commands["server_ok"] = self.server_ok
        self.commands["name_ok"] = self.name_ok
        self.commands["join_ok"] = self.join_ok

    def new_message(self, msg):
        message = msg['msg']
        chat = self.interface.pages["chat_room"].chat_window_widget
        chat.add_message(message)

    def server_crashed(self, msg):
        messagebox.showerror("Server crashed", "Server crashed")
        self.interface.raise_page(self.interface.pages["enter_name"])
        self.client.connected = False

    def host_disconnected(self, msg):
        tkinter.messagebox.showinfo(title="Host disconnected", message="Host disconnected!")
        self.interface.raise_page(self.interface.pages["start"])

    def servers_list(self, msg):
        list = Handler.servers_list_convert(msg["rooms"])
        self.interface.update_servers_list(list)

    def previous_messages(self, msg):
        msgs = msg["messages"]
        for msg in msgs:
            self.interface.pages["chat_room"].chat_window_widget.add_message(msg)

    def messagebox(self, msg):
        msg = msg["text"]
        messagebox.showinfo("Information", msg)
        for entry in self.interface.pages["create"].entries:
            entry.delete(0, tkinter.END)
        self.interface.pages["enter_name"].entries[0].delete(0, tkinter.END)

    def server_ok(self, msg):
        self.interface.load_chat_room()
        for entry in self.interface.pages["create"].entries:
            entry.delete(0, tkinter.END)

    def name_ok(self, msg):
        self.interface.client.name = self.interface.pages["enter_name"].entries[0].get()
        self.interface.raise_page(self.interface.pages["start"])

    def join_ok(self, msg):
        self.interface.load_chat_room()

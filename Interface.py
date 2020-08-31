import tkinter
from tkinter import messagebox, simpledialog
from client import Client
from info_sender import InfoSender
from widgets_creator import WidgetsCreator
from server_messages_handler import Handler
import copy


class Page(tkinter.Frame):

    def __init__(self, root, name):
        tkinter.Frame.__init__(self, root)
        self.name = name
        self.buttons = []
        self.labels = []
        self.entries = []
        self.listboxes = []
        self.canvas = None
        self.chat_window_widget = None


class Interface:
    root = tkinter.Tk()
    root.resizable(False, False)
    root.minsize(width=150, height=150)
    pages = {"start": Page(root, "start"), "choose_server": Page(root, "choose_server"), "create": Page(root, "create"),
             "enter_name": Page(root, "enter_name"), "chat_room": Page(root, "chat_room")}

    def __init__(self, client):
        self.root.protocol('WM_DELETE_WINDOW', self.exit_button)
        self.create_widgets()
        self.raised_page = self.pages["enter_name"]
        self.raise_page(self.pages["enter_name"])
        self.client = client
        self.handler = Handler(self)

    def raise_page(self, page):
        self.raised_page = page
        for p in self.pages.values():
            p.grid_forget()
        page.grid()
        page.tkraise()
        page.focus_set()

    def start(self):
        self.root.mainloop()

    def exit_button(self):
        try:
            InfoSender.disconnect(self.client)
        except Exception:
            pass
        finally:
            self.client.connected = False
            self.handler.run = False
            self.root.destroy()

    def create_widgets(self):
        WidgetsCreator.create_widgets(self)

    def get_server_properties(self, event=None):
        # And send creation of server info to server
        name = self.pages["create"].entries[0].get()
        password = self.pages["create"].entries[1].get()
        capacity = self.pages["create"].entries[2].get()
        InfoSender.create_server(self.client, [name, password, capacity])

    def enter_name_ok_button(self, event=None):
        self.client.connect()
        if not self.client.connected:
            tkinter.messagebox.showerror(title="Error", message="Could not connect to the server")
        else:
            name = self.pages["enter_name"].entries[0].get()
            if name:
                InfoSender.set_name(self.client, name)

    def send_button(self, event=None):
        if self.raised_page == self.pages["chat_room"]:
            text = copy.copy(self.pages["chat_room"].entries[0].get())
            if text != "":
                InfoSender.send_chat_mes(self.client, text)
                self.pages["chat_room"].entries[0].delete(0, 'end')

    def disconnect_button(self):
        InfoSender.leave_chat_room(self.client)
        self.raise_page(self.pages["start"])

    def load_choose_server_page(self):
        self.raise_page(self.pages["choose_server"])
        InfoSender.request_servers(self.client)

    def update_servers_list(self, servers_list):
        self.pages["choose_server"].listboxes[0].delete(0, tkinter.END)
        for server_string in servers_list:
            self.pages["choose_server"].listboxes[0].insert(tkinter.END, server_string)

    def join_server(self):
        server_string = self.pages["choose_server"].listboxes[0].get(tkinter.ANCHOR)
        name = server_string.partition("|")[2].partition("|")[0].strip()
        protected = server_string.partition("|  Protected: ")[2]
        if protected[0:2] == "No":
            InfoSender.join_server(self.client, name)
        elif protected[0:2] == "Ye":
            password = simpledialog.askstring(title="Server is protected", prompt="Enter password: ")
            InfoSender.join_server(self.client, name, password)

    def load_chat_room(self):
        self.pages["chat_room"].chat_window_widget.reset()
        self.raise_page(self.pages["chat_room"])
        self.load_previous_chat_messages()

    def load_previous_chat_messages(self):
        InfoSender.request_previous_messages(self.client)

    def update_chat_messages(self):
        pass


client1 = Client()
interface1 = Interface(client1)
interface1.start()

import tkinter
from chat_window_widget import ChatWindowWidget


class WidgetsCreator:
    @staticmethod
    def create_widgets(interface):
        WidgetsCreator.create_start_page(interface)
        WidgetsCreator.create_create_page(interface)
        WidgetsCreator.create_enter_name_page(interface)
        WidgetsCreator.create_chat_room_page(interface)
        WidgetsCreator.create_choose_server_page(interface)

    @staticmethod
    def create_start_page(interface):
        interface.pages["start"].labels.append(tkinter.Label(interface.pages["start"], text="CHAT"))
        interface.pages["start"].labels[-1].config(font=("Courier", 20))

        interface.pages["start"].buttons.append(
            tkinter.Button(interface.pages["start"], text="Connect to existing server", justify=tkinter.CENTER,
                           command=lambda: interface.load_choose_server_page()))
        interface.pages["start"].buttons.append(
            tkinter.Button(interface.pages["start"], text="Create new server", justify=tkinter.CENTER,
                           command=lambda: interface.raise_page(interface.pages["create"])))
        row = 0
        column = 0
        for label in interface.pages["start"].labels:
            label.grid(row=row, column=column, columnspan=2, padx=5, pady=5)
            row += 1
        for button in interface.pages["start"].buttons:
            button.grid(row=row, column=column, padx=5, pady=5)
            row += 1

    @staticmethod
    def create_create_page(interface):
        interface.pages["create"].labels.append(tkinter.Label(interface.pages["create"], text="Server name:"))
        interface.pages["create"].labels.append(tkinter.Label(interface.pages["create"], text="Password [optional]:"))
        interface.pages["create"].labels.append(tkinter.Label(interface.pages["create"], text="People limit:"))

        interface.pages["create"].buttons.append(
            tkinter.Button(interface.pages["create"], text="Apply", justify=tkinter.CENTER,
                           command=interface.get_server_properties))
        interface.pages["create"].buttons.append(
            tkinter.Button(interface.pages["create"], text="Menu", justify=tkinter.CENTER,
                           command=lambda: interface.raise_page(interface.pages["start"])))

        interface.pages["create"].entries.append(tkinter.Entry(interface.pages["create"]))
        interface.pages["create"].entries.append(tkinter.Entry(interface.pages["create"]))
        interface.pages["create"].entries.append(tkinter.Entry(interface.pages["create"]))

        row = 0
        column = 0
        for label, entry in zip(interface.pages["create"].labels, interface.pages["create"].entries):
            label.grid(row=row, column=column, padx=5, pady=5)
            entry.grid(row=row, column=column + 1, padx=5, pady=5)
            row += 1
        for button in interface.pages["create"].buttons:
            button.grid(row=row, column=0, columnspan=2, padx=5, pady=5)
            row += 1

    @staticmethod
    def create_enter_name_page(interface):
        interface.pages["enter_name"].labels.append(tkinter.Label(interface.pages["enter_name"], text="Enter name:"))
        interface.pages["enter_name"].entries.append(tkinter.Entry(interface.pages["enter_name"]))
        interface.pages["enter_name"].buttons.append(
            tkinter.Button(interface.pages["enter_name"], justify=tkinter.CENTER, text="Ok",
                           command=interface.enter_name_ok_button))

        row = 0
        column = 0
        for label, entry in zip(interface.pages["enter_name"].labels, interface.pages["enter_name"].entries):
            label.grid(row=row, column=column, padx=5, pady=5)
            entry.grid(row=row, column=column + 1, padx=5, pady=5)
            row += 1
        for button in interface.pages["enter_name"].buttons:
            button.grid(row=row, column=0, columnspan=2, padx=5, pady=5)
            row += 1

    @staticmethod
    def create_chat_room_page(interface):
        canvas_width = 400
        canvas_height = 500
        interface.pages["chat_room"].chat_window_widget = ChatWindowWidget(interface.pages["chat_room"], canvas_width,
                                                                           canvas_height)

        interface.pages["chat_room"].entries.append(tkinter.Entry(interface.pages["chat_room"], width=50))
        interface.pages["chat_room"].entries[0].grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        interface.pages["chat_room"].buttons.append(
            tkinter.Button(interface.pages["chat_room"], text="Disconnect", justify=tkinter.CENTER,
                           command=lambda: interface.disconnect_button()))
        interface.pages["chat_room"].buttons.append(
            tkinter.Button(interface.pages["chat_room"], text="Send", justify=tkinter.CENTER,
                           command=lambda: interface.send_button()))

        col = 0
        interface.root.bind('<Return>', interface.send_button)
        for button in interface.pages["chat_room"].buttons:
            button.grid(row=2, column=col, padx=5, pady=5)
            col += 1

    @staticmethod
    def create_choose_server_page(interface):
        interface.pages["choose_server"].buttons.append(
            tkinter.Button(interface.pages["choose_server"], text="Back", justify=tkinter.CENTER,
                           command=lambda: interface.raise_page(interface.pages["start"])))
        interface.pages["choose_server"].buttons.append(
            tkinter.Button(interface.pages["choose_server"], text="Refresh", justify=tkinter.CENTER,
                           command=lambda: interface.load_choose_server_page()))
        interface.pages["choose_server"].buttons.append(
            tkinter.Button(interface.pages["choose_server"], text="Join", justify=tkinter.CENTER,
                           command=lambda: interface.join_server()))
        interface.pages["choose_server"].listboxes.append(
            tkinter.Listbox(interface.pages["choose_server"], height=20, width=55))

        interface.pages["choose_server"].buttons[0].grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.N)
        interface.pages["choose_server"].buttons[2].grid(row=1, column=1, padx=5, pady=5)
        interface.pages["choose_server"].buttons[1].grid(row=0, column=2, padx=5, pady=5, sticky=tkinter.N)
        interface.pages["choose_server"].listboxes[0].grid(row=0, column=1, padx=5, pady=5)

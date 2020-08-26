import tkinter


class ChatWindowWidget:
    def __init__(self, frame, width=400, height=500):
        self.font_size = 15
        self.offset = 5
        self.width = width
        self.height = height
        self.canvas = tkinter.Canvas(frame, bg='#FFFFFF', width=width, height=height,
                                     scrollregion=(0, 0, width, height + 50))
        self.canvas.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.vbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        self.vbar.grid(row=0, column=3, padx=5, pady=5)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)

        self.messages = []
        self.xcord = self.font_size + self.offset
        self.ycord = self.font_size + self.offset

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            self.canvas.xview_scroll(scroll, "units")
        else:
            self.canvas.yview_scroll(scroll, "units")

    def convert_message(self, text):
        new_text = text
        return new_text

    def add_message(self, text):
        text = self.check_resize(text)
        self.messages.append(text)
        self.canvas.create_text(self.xcord, self.ycord, fill="darkblue", font=f"Times {self.font_size} italic bold",
                                text=text,
                                anchor=tkinter.W)
        self.ycord += self.font_size + self.offset

    def check_resize(self, text):
        if self.ycord >= self.height - self.font_size - self.offset:
            self.height += (self.font_size + self.offset)
            self.canvas.config(scrollregion=(0, 0, self.width, self.height + self.offset))
        return str(text)

    def reset(self):
        self.width = 400
        self.height = 500
        self.messages = []
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, self.width, self.height + self.offset))
        self.ycord = self.font_size + self.offset

import tkinter


class ChatWindowWidget:
    def __init__(self, frame, width=400, height=500):
        self.font_size = 15
        self.offset = 8
        self.width = width
        self.height = height
        self.bits_limit = 40
        self.canvas = tkinter.Canvas(frame, bg='#FFFFFF', width=width, height=height,
                                     scrollregion=(0, 0, width, height + 50))
        self.canvas.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.vbar = tkinter.Scrollbar(frame, orient=tkinter.VERTICAL)
        self.vbar.grid(row=0, column=3, padx=5, pady=5)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.vbar.set)

        self.messages = []
        self.xcord = self.font_size + self.offset
        self.ycord = -1 * self.font_size

        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def on_mousewheel(self, event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            self.canvas.xview_scroll(scroll, "units")
        else:
            self.canvas.yview_scroll(scroll, "units")

    def convert_message(self, date, name, text):
        return f"{date}|{name}: {text}"

    def add_message(self, msg):
        self.ycord += self.font_size + self.offset
        new_text, lines = self.add_new_lines(msg[2], msg[1])
        new_msg = self.convert_message(msg[0], msg[1], new_text)
        self.messages.append(new_msg)
        self.canvas.create_text(self.xcord, self.ycord, fill="darkblue", font=f"Times {self.font_size} italic bold",
                                text=new_msg,
                                anchor="nw")
        for _ in range(lines-1):
            self.ycord += self.font_size + self.offset
        self.check_resize(lines)
        self.scroll_down()

    def check_resize(self, lines):
        if self.ycord >= self.height - lines * (self.font_size - self.offset):
            self.height += (self.font_size + self.offset)
            self.canvas.config(scrollregion=(0, 0, self.width, self.height + self.offset))

    def add_new_lines(self, text, name):
        char_counter = 8 + len(name)
        words = text.split()
        new_words = []
        lines = 1
        for word in words:
            char_counter += len(word)
            if char_counter >= self.bits_limit:
                new_words.append("\n")
                lines += 1
                new_words.append(word)
                char_counter = len(word)
            else:
                new_words.append(word)
        return r" ".join(new_words), lines

    def reset(self):
        self.width = 400
        self.height = 500
        self.messages = []
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0, 0, self.width, self.height + self.offset))
        self.ycord = self.font_size + self.offset

    def scroll_down(self):
        self.canvas.yview_moveto('1.0')

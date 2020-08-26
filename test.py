from tkinter import *

root = Tk()
frame = Frame(root, width=300, height=300)
frame.grid()
bt = Button(frame, text="xd", command=lambda: create_canvas(x))
bt.pack()
x = [500]
canvas = Canvas(frame, bg='#FFFFFF', width=300, height=300, scrollregion=(0, 0, x[0], x[0]))
vbar = Scrollbar(frame, orient=VERTICAL)
vbar.pack(side=RIGHT, fill=Y)
vbar.config(command=canvas.yview)
canvas.config(yscrollcommand=vbar.set)
canvas.pack(side=LEFT, expand=True, fill=BOTH)


def create_canvas(x):
    canvas.create_text(20,x[0]-20,fill="darkblue",font="Times 20 italic bold",text="Helllo")
    canvas.config(scrollregion=(0, 0, x[0], x[0]))
    x[0] += 1000

root.mainloop()
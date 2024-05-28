from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry('300x200')
root.title('my window')
btn1 = ttk.Button(root, text='按钮1')
btn1.pack(pady=10)
# btn2 = Button(root, text='按钮2', bg='red')
# btn2.pack(anchor=S)
# btn3 = Button(root, text='按钮3', bg='red')
# btn3.pack(anchor=NE)
# btn4 = Button(root, text='按钮4', bg='red')
# btn4.pack()
root.mainloop()

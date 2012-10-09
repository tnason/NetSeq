import Tkinter
from Tkinter import *
import ttk
from ttk import *

root = Tkinter.Tk()

style = ttk.Style()
style.configure("TButton", background="black", active="black", focus="black")

b1 = ttk.Button(text="Test1")
b1.pack()

root.mainloop()


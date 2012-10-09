import Tkinter
from Tkinter import *
import ttk
from ttk import *

root = Tkinter.Tk()

style = ttk.Style()
style.configure("TLabel", foreground="black", background="white")

l1 = ttk.Label(text="Test1")
l2 = ttk.Label(text="Test2")
l1.pack()

root.mainloop()

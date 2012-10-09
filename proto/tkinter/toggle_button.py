import Tkinter

root = Tkinter.Tk()

def toggle(button, variable):
    if variable.get():
        button.config(text='On')
    else:
        button.config(text='Off')

v1 = Tkinter.BooleanVar()
v1.set(False)
b1 = Tkinter.Checkbutton(root, text='Off', variable=v1, indicatoron=False,
                         selectcolor='', command=lambda : toggle(b1, v1))
b1.pack(padx=50, pady=50)

root.mainloop()

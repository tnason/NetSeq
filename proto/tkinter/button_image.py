from Tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.photo=PhotoImage(file="blue.gif")
        self.quitButton = Button( self, text='Quit',
            command=self.quit )
        self.quitButton.config(image=self.photo)
        self.quitButton.grid()

app = Application()
app.master.title("Sample application")
app.mainloop()


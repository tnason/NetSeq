import kivy
from kivy.app import App
from kivy.uix.button import Button
import Tkinter
import tkFileDialog

def callback(instance):
    # Explictly make and then hide the Tkinter root window
    root = Tkinter.Tk()
    root.withdraw()

    # Get the filename from the dialog
    filename = tkFileDialog.askopenfilename()

    # Interact with kivy
    instance.text = "You selected\n" + filename + "\n"
    instance.text += "Press again to change"

class ButtonApp(App):
    def build(self):
        button = Button(text='Select a file', font_size=12)
        button.bind(on_press=callback)
        return button

if __name__ == "__main__":
    ButtonApp().run()

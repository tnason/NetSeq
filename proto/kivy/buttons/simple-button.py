import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

def callback(instance):
    print "I was pressed!"

class ButtonApp(App):
    def build(self):
        button = Button(text='Send frequency', font_size=14)
        button.bind(on_press=callback)
        return button

if __name__ == "__main__":
    ButtonApp().run()

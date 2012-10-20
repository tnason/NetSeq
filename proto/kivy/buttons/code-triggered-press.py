import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from time import sleep

def press_callback(instance):
    print "I was pressed!"
    sleep(3)
    instance.dispatch('on_release')

def release_callback(instance):
    print "Release callback!"

class ButtonApp(App):
    def build(self):
        button = ToggleButton(text='Send frequency', font_size=14)
        button.bind(on_press=press_callback)
        button.bind(on_release=release_callback)
        return button

if __name__ == "__main__":
    ButtonApp().run()

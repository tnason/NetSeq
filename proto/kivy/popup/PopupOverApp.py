from kivy.app import App
from kivy.uix.popup import *
from kivy.uix.label import *
from kivy.uix.button import *

class PairSeqApp(App):
    def build(self):
        # 'size' below sets the size of this
        # Get rid of 'size', add 'size_hint' as (1,1) to cover whole
        # screen with our popup
        popup = Popup(title='Test popup',
            size_hint=(1, 1),
            auto_dismiss=False)
        # Set the popup's content to a 'close' button
        popup.content = Button(text="Close me!")
        popup.content.bind(on_press=popup.dismiss)
        popup.open()
        return 0

if __name__ == '__main__':
    # Start the apps like this to make sure they don't exit immediately
    PairSeqApp().run()


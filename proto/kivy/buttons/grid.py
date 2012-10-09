import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button

NUM_ROWS = 16
NUM_COLS = 16

class ButtonGrid(Widget):

    def __init__(self):
        self.root = Widget(size=[self.get_root_window().width, self.get_root_window().height])
        self.buttons = []

    def makeButtons(self):
        root = self.root
        buttonWidth = self.width / NUM_COLS
        buttonHeight = self.height / NUM_ROWS
        print "widget width: ", self.width
        print "widget height: ", self.height
        print "button width: ", buttonWidth
        print "button height: ", buttonHeight
        for row in range(0, NUM_ROWS):
            self.buttons.append([])
            for col in range(0, NUM_COLS):
                newButton = Button(width=buttonWidth, height=buttonHeight,
                                    x=col*buttonWidth, y=row*buttonHeight)
                self.buttons[row].append(newButton)
                root.add_widget(newButton)
        return root

class Builder:
    def build():
        ButtonGrid = new Widget()

class ButtonGridApp(App):
    def build(self):
        grid = ButtonGrid()
        return grid.makeButtons()

if __name__ == "__main__":
    ButtonGridApp().run()


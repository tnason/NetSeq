from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.uix.filechooser import *

class TabbedPanelApp(App):
    def build(self):
        self.fciv = FileChooserIconView(on_submit = self.printPath)
        print "Hello!"
        return self.fciv

    def printPath(self):
        print "Path: ", self.fciv.path

if __name__ == '__main__':
    TabbedPanelApp().run()


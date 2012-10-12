from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('main_layout.kv')

def get_widget_by_id(parent, name):
    widget_found = False
    widget_result = None

    if (parent.children != None) :
        for child in parent.children:
            if (child.id != None):
                print "Next ID: ", child.id
            widget_result = get_widget_by_id(child, name)
            if (widget_result != None):
                widget_found = True
   
    if (parent.id == name):
        widget_found = True
        widget_result = parent
    
    return widget_result

class MyWidget(BoxLayout):
    pass

class NetSeqApp(App):
    def build(self):
        my_widget = MyWidget()
        # button_grid = get_widget_by_id(my_widget, "notes_layout")
        # print button_grid
        return my_widget

if __name__ == "__main__":
    NetSeqApp().run()

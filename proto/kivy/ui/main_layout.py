from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout

class MyWidget(Widget):
    def __init__(self):
        super(MyWidget, self).__init__()
        
        # For each element of the GUI, make sure to
        # 1. Create a unique reference attached to this object for
        #   future manipulation. e.g. self.main_box = main_box after you've
        #   created a BoxLayout called main_box

        # Interesting things about Kivy UI programming:
        # 1. y starts counting from bottom left
        # 2. set size_hint to '[None, None]' for all new widgets if defining
        #       the size and manually

        # MAIN LAYOUT
        main_layout = FloatLayout(size=[800,600], orientation='horizontal')
        self.main_layout = main_layout
        self.add_widget(main_layout)

        # TABS WITH GAME CONTROL
        # Tabbed panel for music, settings, network
        # Y-position of tabbed panel depends on tab height!
        tabs = TabbedPanel(tab_width=50, size=[160, 480], pos=[0, 120],
                           size_hint=(None, None))
        self.tabs = tabs
        main_layout.add_widget(tabs)

        # Music tab
        music_button = Button(text="Music things")
        tabs.default_tab_content = music_button
        tabs.default_tab.text = "Music"

        # Network tab
        network_tab = TabbedPanelHeader(text="Net")
        tabs.add_widget(network_tab)
        network_button = Button(text="Network things")
        network_tab.content = network_button

        # Global tab
        global_tab = TabbedPanelHeader(text="Global")
        tabs.add_widget(global_tab)
        global_button = Button(text="Global things")
        global_tab.content = global_button
        # END TABS

        # RIGHT-SIDE LAYOUT: NOTES GRID AND PLAYBACK UI
        music_layout = FloatLayout(size=[640, 600], pos=[161, 0],
                                   size_hint=[None, None])
        self.music_layout = music_layout
        main_layout.add_widget(music_layout)

        # NOTES GRID
        notes = Button(text="Notes here", size=[640, 480], 
                       pos=[161, 121], size_hint=[None, None])
        music_layout.add_widget(notes)

        prenote_padding = 30
        posnote_padding = 30
        notes_matrix = []
        
        x = notes.x
        y = notes.y
        width = notes.width
        height = notes.height
        print 'x: ', x
        print 'y: ', y
        print 'w: ', width
        print 'h: ', height
        print 'pos: ', music_layout.pos

        # PLAYBACK BUTTONS
        playback = Button(text="For playback", size=[640, 120], 
                          size_hint=[None, None], pos=[161, 0])
        music_layout.add_widget(playback)

        

class NetSeqApp(App):
    def build(self):
        my_widget = MyWidget()
        # button_grid = get_widget_by_id(my_widget, "notes_layout")
        # print button_grid
        return my_widget

if __name__ == "__main__":
    NetSeqApp().run()

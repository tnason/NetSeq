import pyo
from pyo import *
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
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput

class MyWidget(Widget):

    def __init__(self):
        super(MyWidget, self).__init__()
        
        self.cos_table = CosTable([(0,0), (100,1), (1000,.25), (8191,0)])
        self.osc_out = Osc(table=self.cos_table, freq=440)

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
        network_layout = BoxLayout(orientation="vertical", padding=10)
        server_button = Button(text="Start server")
        ip_label = Label(text="Your IP is\n123.234.456.789");
        client_label = Label(text="Connect to server: ");
        server_ip_input = TextInput(text="Enter server IP")
        network_layout.add_widget(server_button)
        network_layout.add_widget(ip_label)
        network_layout.add_widget(client_label)
        network_layout.add_widget(server_ip_input)
        network_tab.content = network_layout

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
        # Right now Kivy isn't really paying attention to button size and
        # padding. Later on, we'll fix this with a FloatLayout
        note_rows = note_cols = 8
        padding_between = 5
        note_grid = GridLayout(size=[640, 480], pos=[161, 121], 
                               size_hint=[None, None], rows=note_rows, 
                               cols=note_cols, padding=padding_between)
        music_layout.add_widget(note_grid)

        edge_padding = 30

        grid_start_x = note_grid.x + edge_padding
        grid_end_x = note_grid.right - edge_padding
        grid_start_y = note_grid.y + edge_padding
        grid_end_y = note_grid.top - edge_padding
        notes_matrix = []

        note_width = grid_end_x - grid_start_x - padding_between * \
                    (note_rows - 1)
        note_height = grid_end_y - grid_start_y - padding_between * \
                      (note_rows - 1)

        for row in range(0, note_rows):
            for col in range(0, note_cols):
                new_id = str(row) + "," + str(col)
                new_button = ToggleButton(text=new_id, id=new_id, 
                                          width=note_width, 
                                          height=note_height)
                new_button.bind(on_press=self.play_note)
                note_grid.add_widget(new_button)
        
        # PLAYBACK BUTTONS
        playback = Button(text="For playback", size=[640, 120], 
                          size_hint=[None, None], pos=[161, 0])
        music_layout.add_widget(playback)

    def play_note(self, instance):
        if instance.state == "down":
            print "Playing!"
            self.osc_out.out()
        else:
            print "Stopping!"
            self.osc_out.stop()

class NetSeqApp(App):
    def build(self):
        my_widget = MyWidget()
        # button_grid = get_widget_by_id(my_widget, "notes_layout")
        # print button_grid
        return my_widget

if __name__ == "__main__":
    # VERY IMPORTANT that we initialize the server here instead of below
    # Otherwise we get a segmentation fault with all kinds of errors
    s = Server().boot()
    s.start()
    NetSeqApp().run()

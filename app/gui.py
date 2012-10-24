from kivy.app import App
from kivy.uix.widget import Widget
from audio.music_player import Note
from audio.music_player import MusicPlayer
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelHeader
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider

class GUI(Widget):
    """Widget for all user interaction with sequencer"""

    def __init__(self, music_player, network):
        """Create main GUI

        Arguments:
        music_player -- audio generator for full application
        network -- network client and server handler

        """
        super(GUI, self).__init__()

        WINDOW_WIDTH = 800
        WINDOW_HEIGHT = 600

        OUTER_PADDING = 20

        # BUTTON GRID
        NOTE_BUTTON_WIDTH = 50
        NOTE_BUTTON_HEIGHT = 50
        NOTE_BUTTON_PADDING = 5
        ROW_LABEL_WIDTH = 30
        ROW_LABEL_HEIGHT = NOTE_BUTTON_HEIGHT
        ROW_LABEL_FONT_SIZE = 14
        NOTE_BUTTON_ROWS = 8
        NOTE_BUTTON_COLS = 8

        GRID_WIDTH = NOTE_BUTTON_PADDING + ROW_LABEL_WIDTH + \
                     NOTE_BUTTON_PADDING + (NOTE_BUTTON_COLS * 
                     (NOTE_BUTTON_WIDTH + NOTE_BUTTON_PADDING))
        GRID_HEIGHT = NOTE_BUTTON_PADDING + (NOTE_BUTTON_ROWS * 
                      (NOTE_BUTTON_HEIGHT + NOTE_BUTTON_PADDING))
        GRID_X = OUTER_PADDING
        GRID_Y = WINDOW_HEIGHT - OUTER_PADDING - GRID_HEIGHT

        # For each row, create labels and notes
        self.row_labels = []
        self.notes = []

        row_top = GRID_Y + GRID_HEIGHT

        for row in range(0, NOTE_BUTTON_ROWS):
            col_x = GRID_X + NOTE_BUTTON_PADDING

            # Make label for row
            row_label = Label(text=str(row), width=ROW_LABEL_WIDTH, 
                              height=ROW_LABEL_HEIGHT, 
                              text_size=[ROW_LABEL_WIDTH, ROW_LABEL_HEIGHT],
                              font_size=ROW_LABEL_FONT_SIZE, halign='center',
                              valign='middle')
            row_label.x = col_x
            row_label.top = row_top
            self.add_widget(row_label)
            self.row_labels.append(row_label)

            col_x = col_x + ROW_LABEL_WIDTH + NOTE_BUTTON_PADDING
            
            # Create all buttons for row
            row_notes = []
            for col in range(0, NOTE_BUTTON_COLS):
                col_button = ToggleButton(width=NOTE_BUTTON_WIDTH,
                                          height=NOTE_BUTTON_HEIGHT)
                col_button.x = col_x
                col_button.top = row_top
                row_notes.append(col_button)
                self.add_widget(col_button)
                col_x = col_x + NOTE_BUTTON_WIDTH + NOTE_BUTTON_PADDING
                
            self.notes.append(row_notes)
            row_top = row_top - NOTE_BUTTON_PADDING - NOTE_BUTTON_HEIGHT

        # PLAYBACK MENU
        PLAYBACK_X = OUTER_PADDING
        PLAYBACK_Y = OUTER_PADDING
        PLAYBACK_WIDTH = GRID_WIDTH
        PLAYBACK_HEIGHT = WINDOW_HEIGHT - OUTER_PADDING - GRID_HEIGHT - \
                          OUTER_PADDING - OUTER_PADDING
        PLAYBACK_CENTER_Y = PLAYBACK_Y + (PLAYBACK_HEIGHT / 2)

        PLAY_BUTTON_WIDTH = 50
        PLAY_BUTTON_HEIGHT = 50
        PLAYALL_BUTTON_WIDTH = 50
        PLAYALL_BUTTON_HEIGHT = 50
        PLAYALL_BUTTON_FONT_SIZE = 8
        PAGE_BUTTON_WIDTH = 25
        PAGE_BUTTON_HEIGHT = 30
        NUM_PAGE_BUTTONS = MusicPlayer.NUM_PAGES
        PAGE_LABEL_WIDTH = (PAGE_BUTTON_WIDTH * NUM_PAGE_BUTTONS)
        PAGE_LABEL_HEIGHT = 20
        PAGE_LABEL_FONT_SIZE = 10
        PAGE_LABEL_OFFSET = 5
        TRACK_BUTTON_WIDTH = 30
        TRACK_BUTTON_HEIGHT = 40
        NUM_TRACK_BUTTONS = MusicPlayer.NUM_TRACKS
        NUM_PLAYBACK_ELEMENTS = 4

        PLAYBACK_PADDING = (PLAYBACK_WIDTH - (PAGE_BUTTON_WIDTH * 
                            NUM_PAGE_BUTTONS) - (PLAY_BUTTON_WIDTH) - 
                            (TRACK_BUTTON_WIDTH * NUM_TRACK_BUTTONS) - 
                            PLAYALL_BUTTON_WIDTH) / (NUM_PLAYBACK_ELEMENTS + 1)
        
        # Play/pause button
        PLAY_BUTTON_X = PLAYBACK_X + PLAYBACK_PADDING
        play_button = Button(width=PLAY_BUTTON_WIDTH, 
                             height=PLAY_BUTTON_HEIGHT)
        play_button.x = PLAY_BUTTON_X
        play_button.center_y = PLAYBACK_CENTER_Y
        self.play_button = play_button
        self.add_widget(play_button)

        # Button to play all pages
        playall_button = Button(width=PLAYALL_BUTTON_WIDTH,
                                height=PLAYALL_BUTTON_HEIGHT,
                                text="Play all", 
                                text_size=[PLAYALL_BUTTON_WIDTH, 
                                    PLAYALL_BUTTON_HEIGHT], 
                                font_size=PLAYALL_BUTTON_FONT_SIZE,
                                halign='center', valign='middle')
        playall_button.x = play_button.right + PLAYBACK_PADDING
        playall_button.center_y = PLAYBACK_CENTER_Y
        self.playall_button = playall_button
        self.add_widget(playall_button)

        # Page selection buttons
        self.page_buttons = []
        page_buttons = []
        page_label = Label(text="Page Select", text_size=[PAGE_LABEL_WIDTH, 
                           PAGE_LABEL_HEIGHT], font_size=PAGE_LABEL_FONT_SIZE,
                           width=PAGE_LABEL_WIDTH, height=PAGE_LABEL_HEIGHT,
                           halign='center', valign='middle')
        page_button_x = playall_button.right + PLAYBACK_PADDING
        page_label.x = page_button_x
        page_label.top = PLAYBACK_CENTER_Y - (PAGE_BUTTON_HEIGHT / 2) - \
                         PAGE_LABEL_OFFSET
        self.add_widget(page_label)
        for page in range(0, NUM_PAGE_BUTTONS):
            page_button = ToggleButton(width=PAGE_BUTTON_WIDTH,
                                       height=PAGE_BUTTON_HEIGHT)
            page_button.x = page_button_x
            page_button.center_y = PLAYBACK_CENTER_Y
            page_buttons.append(page_button)
            self.add_widget(page_button)
            page_button_x += PAGE_BUTTON_WIDTH

        self.page_buttons = page_buttons

        # Track selection buttons
        track_buttons = []
        self.track_buttons = []
        track_button_x = page_buttons[len(page_buttons) - 1].right + \
                         PLAYBACK_PADDING
        for track in range(0, NUM_TRACK_BUTTONS):
            track_button = ToggleButton(width=TRACK_BUTTON_WIDTH, 
                                        height=TRACK_BUTTON_HEIGHT)
            track_button.x = track_button_x
            track_button.center_y = PLAYBACK_CENTER_Y
            track_buttons.append(track_button)
            self.add_widget(track_button)
            track_button_x += TRACK_BUTTON_WIDTH
        
        self.track_buttons = track_buttons        

        # SETTINGS TABS
        TABS_X = OUTER_PADDING + GRID_WIDTH + OUTER_PADDING
        TABS_Y = GRID_Y
        TABS_WIDTH = WINDOW_WIDTH - OUTER_PADDING - GRID_WIDTH - \
                     OUTER_PADDING - OUTER_PADDING
        TABS_HEIGHT = GRID_HEIGHT
        # Note: it's a good idea to make these tabs the size of our icons,
        # which is 48x48
        TAB_HEADER_WIDTH = 48
        TAB_HEADER_HEIGHT = TAB_HEADER_WIDTH
        TAB_HEADER_FONT_SIZE = 20
        SECTION_LABEL_FONT_SIZE = 10
        SECTION_LABEL_HEIGHT = 30
        ELEMENT_LABEL_FONT_SIZE = 8
        ELEMENT_LABEL_HEIGHT = 20
        TAB_CONTENT_HEIGHT = TABS_HEIGHT - TAB_HEADER_HEIGHT
        TAB_CONTENT_TOP = TABS_Y + TAB_CONTENT_HEIGHT

        # Element is button, label, etc. Section is vertical group of elements
        TAB_SECTION_PADDING = 20
        TAB_ELEMENT_PADDING = 10

        # Create main tabbed panel
        tabs = TabbedPanel(tab_width=TAB_HEADER_WIDTH, 
                           tab_height=TAB_HEADER_HEIGHT, width=TABS_WIDTH, 
                           height=TABS_HEIGHT)
        tabs.x = TABS_X
        tabs.y = TABS_Y
        self.add_widget(tabs)
        self.tabs = tabs

        # Music tab (default)
        # TODO: make these paths absolute?
        music_tab_content = Widget(width=TABS_WIDTH, height=TAB_CONTENT_HEIGHT)
        tabs.default_tab_content = music_tab_content
        tabs.default_tab.text = ""
        # TODO: replace this image with 48x48
        tabs.default_tab.background_normal = \
            "../assets/icons/audio-keyboard.png"
        tabs.default_tab.background_down = \
            "../assets/icons/audio-keyboard.png"

        # Global music options
        global_music_label = Label(text="Global", 
                                   font_size=SECTION_LABEL_FONT_SIZE,
                                   width=TABS_WIDTH, 
                                   height=SECTION_LABEL_HEIGHT,
                                   valign='middle')
        global_music_label.center_x = tabs.center_x
        global_music_label.top = TAB_CONTENT_TOP - TAB_SECTION_PADDING
        music_tab_content.add_widget(global_music_label)
        
        global_volume_slider = Slider(min=MusicPlayer.MIN_TEMPO, 
                                      max=MusicPlayer.MAX_TEMPO,
                                      value=music_player.tempo,
                                      orientation='horizontal')


        # Network tab
        network_tab = TabbedPanelHeader()
        network_tab.text = ""
        network_tab.background_normal = \
            "../assets/icons/network-wired.png"
        network_tab.background_down = \
            "../assets/icons/network-wired.png"
        tabs.add_widget(network_tab)

        # System options tab
        system_tab = TabbedPanelHeader()
        system_tab.background_normal = \
            "../assets/icons/computer-4.png"
        system_tab.background_down = \
            "../assets/icons/computer-4.png"
        tabs.add_widget(system_tab)

    def __del__(self):
        """Destroy this instance of the GUI"""
        pass

    def set_note(self, note):
        """Set a note in note grid to on or off

        Arguments:
        note -- note with position in GUI and whether to turn on

        """
        pass

    def set_volume(self, track_index, volume):
        """Redraw volume slider for a track at new value

        Arguments:
        track_index -- which track to set slider for
        volume -- new volume for the track

        """
        pass

    def set_reverb(self, track_index, reverb):
        """Redraw rever slider for a track at new value

        Arguments:
        track_index -- which track to redraw slider for
        reverb -- new value for reverb

        """
        pass

    def set_tempo(self, tempo):
        """Redraw global tempo at new value

        Arguments:
        tempo -- new value for tempo

        """
        pass

    def new_session(self):
        """Redraw entirety of UI in response to session load"""
        pass

    def move_playhead(self, column):
        """Move playhead to new column

        Arguments:
        column -- destination column for playhead
        
        """
        pass

    def break_from_server(self):
        """Show window describing disconnected server"""
        pass

class NetSeqApp(App):
    """Kivy application that kicks off GUI"""
    
    def build(self):
        """Build GUI"""
        music_player = MusicPlayer()
        gui_widget = GUI(None, None)
        return gui_widget

if __name__ == "__main__":
    NetSeqApp().run()

from kivy.app import App
from kivy.uix.widget import Widget
from audio.music_player import Note
from audio.music_player import MusicPlayer
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

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

        PAGE_BUTTON_WIDTH = 40
        PAGE_BUTTON_HEIGHT = 40
        NUM_PAGE_BUTTONS = MusicPlayer.NUM_PAGES
        PLAY_BUTTON_WIDTH = 50
        PLAY_BUTTON_HEIGHT = 50
        TRACK_BUTTON_WIDTH = 40
        TRACK_BUTTON_HEIGHT = 40
        NUM_TRACK_BUTTONS = MusicPlayer.NUM_TRACKS
        PLAYALL_BUTTON_WIDTH = 50
        PLAYALL_BUTTON_HEIGHT = 50

        PLAYBACK_PADDING = PLAYBACK_WIDTH - (PAGE_BUTTON_WIDTH * 
                           NUM_PAGE_BUTTONS) - (

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
        gui_widget = GUI(None, None)
        return gui_widget

if __name__ == "__main__":
    NetSeqApp().run()

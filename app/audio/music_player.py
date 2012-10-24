class MusicPlayer:
    """Playback engine for sequencer samples and sounds"""

    NUM_PAGES = 8
    NUM_TRACKS = 3
    
 
    def __init__(self):
        """Constructor for music_player"""
        """Make sure to call add_network_handler once initialized"""
        self.instruments = [] #instrument/track volume is here
        self.tempo = 120 #BPM (for now)
        self.global_volume = 0.75 #between 0 and 1
        self.page_index = 0 #1st page
        self.play_all = False
        self.playhead_index = 0 #how do we want to implement this?
        

    def add_network_handler(self, network_handler):
        self.network_handler = network_handler
        
    """playback methods"""
    def play_page(self, page_id):
        pass

    def play_all(self):
        pass

    def pause(self):
        pass

    def set_session(self, Session):
        """used to load a session into the music player"""
        pass

    """GUI-called track modification functions"""
    def gui_set_note(self, Note):
        pass

    def gui_set_volume(self, track_id, volume):
        pass
    
    def gui_set_global_volume(self, volume):
        pass

    def gui_set_tempo(self, tempo):
        pass

    def gui_set_reverb(self, track_id, reverb):
        pass

    """network-called track modification functions"""
    def network_set_note(self, Note):
        pass

    def network_set_volume(self, track_id, volume):
        pass

    def network_set_tempo(self, tempo):
        pass

    def network_set_reverb(self, track_id, reverb):
        pass

    """getter methods"""
    def get_session(self):
        pass

    """getter methods for GUI"""
    def get_reverb(self, track_id):
        pass

    def get_volume(self, track_id):
        pass

    def get_global_volume(self):
        pass

    def get_tempo(self):
        pass

    def get_note(self, track_id, page_index, position, pitch):
        pass

    def get_current_page(self):
        pass

    def get_current_track(self):
        pass
        

class Note:
    """Data for turning note on or off"""

    def __init__(self, track_id, page_index, column, row, turn_on):
        """Create Note corresponding to location and whether to turn on"""
        self.track_id = track_id
        self.page_index = page_index
        self.column = column
        self.row = row
        self.turn_on = turn_on

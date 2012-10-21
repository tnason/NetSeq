class MusicPlayer:
    """Playback engine for sequencer samples and sounds"""

    NUM_PAGES = 8
    NUM_TRACKS = 3

class Note:
    """Data for turning note on or off"""

    def __init__(self, track_id, page_index, column, row, turn_on):
        """Create Note corresponding to location and whether to turn on"""
        self.track_id = track_id
        self.page_index = page_index
        self.column = column
        self.row = row
        self.turn_on = turn_on

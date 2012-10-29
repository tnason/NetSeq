from instrument import WaveInstrument
from pyo import *

class MusicPlayer:
    """Playback engine for sequencer samples and sounds"""

    NUM_PAGES = 8
    NUM_ROWS = 8
    NUM_COLS = 8
    NUM_TRACKS = 3
    NUM_BEATS = NUM_PAGES * NUM_COLS

    SECONDS_PER_MIN = 60.0

    # Parameters for GUI to build sliders
    MIN_TEMPO = 40.0
    MAX_TEMPO = 240.0
    MIN_VOLUME = 0.0
    MAX_VOLUME = 1.0
    MIN_REVERB = 0.0
    MAX_REVERB = 1.0 

    # Instrument descriptive constants
    WAVETABLE_A = 0
    WAVETABLE_B = 1
    DRUM_KIT = 2

    def __init__(self):
        """Constructor for music_player"""
        """Make sure to call add_network_handler once initialized"""
        self.instruments = [] #instrument/track volume is here
        self.tempo = 120.0 #BPM (for now)
        self.global_volume = 0.75 #between 0 and 1
        self.page_index = 0 #1st page
        self.play_all = False
        self.playhead_index = 0
        self.beat_index = 0

        self.server = Server()
        self.server.boot()
        self.server.start()

        metronome_time = self.SECONDS_PER_MIN / self.tempo
        print "@@ metro time: ", metronome_time
        self.metronome = Metro(time=metronome_time)
        self.metronome_callback = TrigFunc(self.metronome, function=self.step)
        
        # Create instruments
        wavetable_a = WaveInstrument(self, WaveInstrument.BASS)
        wavetable_b = WaveInstrument(self, WaveInstrument.LEAD)
        
        self.instruments.append(wavetable_a)
        self.instruments.append(wavetable_b)

        # Initialize master mixer
        self.master_mixer = Mixer(outs=1)   
        for inst_index in range(0, len(self.instruments)):
            instrument = self.instruments[inst_index]
            generator = instrument.get_generator()
            self.master_mixer.addInput(inst_index, generator)
            self.master_mixer.setAmp(inst_index, 0, 1)
        
        self.master_mixer.out()

    def step(self):
        """ Step the music player through next beat """
        print "@@ Music player step"

        # Move playhead one step
        self.playhead_index = (self.playhead_index + 1) % self.NUM_COLS

        # Play next step for each instrument       
        for instrument in self.instruments:
            instrument.play_step()
        
        # Determine next beat to play
        if (self.play_all == True):
            self.beat_index = (self.beat_index + 1) % self.NUM_BEATS
        elif (self.play_all == False):
            self.beat_index = (self.page_index * self.NUM_COLS) +\
                              self.playhead_index

    def add_network_handler(self, network_handler):
        self.network_handler = network_handler
        
    """playback methods"""
    def play(self):
        print "@@ Music Player play method"
        self.metronome.play()

    def play_all(self):
        #start metronome
        pass

    def pause(self):
        self.metronome.stop()

    def set_session(self, session):
        """used to load a session into the music player"""
        pass

    """GUI-called track modification functions"""
    def gui_set_note(self, note):
        instrument = self.instruments[note.track_id]
        instrument.set_note(note)

    def gui_set_volume(self, track_id, volume):
        pass
    
    def gui_set_global_volume(self, volume):
        pass

    def gui_set_tempo(self, tempo):
        #self.playhead_metronome.setTime(SECONDS_PER_MIN/tempo)
        #self.tempo = tempo
        pass

    def gui_set_reverb(self, track_id, reverb):
        pass

    """network-called track modification functions"""
    def network_set_note(self, note):
        pass

    def network_set_volume(self, track_id, volume):
        pass

    def network_set_tempo(self, tempo):
        #self.playhead_metronome.setTime(SECONDS_PER_MIN/tempo)
        #self.tempo = tempo
        pass

    def network_set_reverb(self, track_id, reverb):
        pass

    """getter methods"""
    def get_session(self):
        pass

    """getter methods for GUI"""
    def get_reverb(self, track_id):
        # TODO: return non-dummy value
        return 0.0

    def get_volume(self, track_id):
        # TODO: return non-dummy value
        return 0.0

    def get_global_volume(self):
        pass

    def get_tempo(self):
        pass

    def get_note(self, track_id, page_index, position, pitch):
        pass

    def get_current_page(self, track_id):
        instrument = self.instruments[track_id]
        notes = instrument.get_page(self.page_index)
        return notes

class Note:
    """Data for turning note on or off"""

    def __init__(self, track_id, page_index, column, row, turn_on):
        """Create Note corresponding to location and whether to turn on"""
        self.track_id = track_id
        self.page_index = page_index
        self.column = column
        self.row = row
        self.turn_on = turn_on

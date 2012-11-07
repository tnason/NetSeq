from instrument import WaveInstrument, DrumInstrument
from instrument import WaveInstrumentData, DrumInstrumentData
from pyo import Mixer, Server, Metro, TrigFunc

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
        """Make sure to call add_gui once initialized"""
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
        self.metronome = Metro(time=metronome_time)
        self.metronome_callback = TrigFunc(self.metronome, function=self.step)
        
        # Create instruments
        wavetable_a = WaveInstrument(self, WaveInstrument.BASS)
        wavetable_b = WaveInstrument(self, WaveInstrument.LEAD)
        drums = DrumInstrument(self)
        
        self.instruments.append(wavetable_a)
        self.instruments.append(wavetable_b)
        self.instruments.append(drums)

        self.mixer_setup()
    
    def mixer_setup(self):
        # Combine all tracks in mixer
        self.track_mixer = Mixer(outs=1)
        for inst_index in range(0, len(self.instruments)):
            instrument = self.instruments[inst_index]
            generator = instrument.get_generator()
            self.track_mixer.addInput(inst_index, generator)
            self.track_mixer.setAmp(inst_index, 0, instrument.get_volume())
        
        # Prepare master output
        self.master_out = Mixer(outs=1, chnls=2)
        self.master_out.addInput(0, self.track_mixer[0])
        self.master_out.setAmp(0, 0, self.global_volume)
        self.master_out.out()

    def add_gui(self, gui):
        """ Sets the GUI that this music player must instruct to update playhead.
        Must be called right after constructor before operation.

        Arguments:
        gui: GUI object monitoring this player

        """
        self.gui = gui
    
    def step(self):
        """ Step the music player through next beat """
        # Set GUI to reflect current beat
        self.gui.update_playhead()
        
        # Play step for instruments
        for instrument in self.instruments:
            instrument.play_step()

        # For next iteration, increment playhead and beat indices
        self.playhead_index = (self.playhead_index + 1) % self.NUM_COLS
        if (self.play_all == True):
            self.beat_index = (self.beat_index + 1) % self.NUM_BEATS
        elif (self.play_all == False):
            self.beat_index = (self.page_index * self.NUM_COLS) +\
                              self.playhead_index

    def add_network_handler(self, network_handler):
        self.network_handler = network_handler
        
    """playback methods"""
    def play(self):
        self.metronome.play()

    def pause(self):
        for instrument in self.instruments:
            instrument.pause()
        self.metronome.stop()

    def set_session(self, session):
        """used to load a session into the music player"""
        # Reload pertinent MusicPlayer variables
        self.set_tempo(session.tempo)

        # Reconstruct each instrument from session data
        self.instruments = []
        instrument_data = session.instrument_data
        for data in instrument_data:
            volume = data.volume
            reverb_mix = data.reverb_mix
            notes = data.notes
            if isinstance(data, WaveInstrumentData):
                wavetype = data.wavetype
                wave_instrument = WaveInstrument(self, wavetype, volume, 
                                                 reverb_mix, notes)
                self.instruments.append(wave_instrument)
            elif isinstance(data, DrumInstrumentData):
                drum_instrument = DrumInstrument(self, volume, reverb_mix,
                                                 notes)
                self.instruments.append(drum_instrument)

        # Reload mixer to reflect new instruments
        self.mixer_setup()

    """ Modifiers """
    def set_note(self, note):
        instrument = self.instruments[note.track_id]
        instrument.set_note(note)

    def set_global_volume(self, volume):
        self.global_volume = volume
        self.master_out.setAmp(0, 0, volume)

    def set_volume(self, track_id, volume):
        self.instruments[track_id].set_volume(volume)
        self.track_mixer.setAmp(track_id, 0, volume)
    
    def set_reverb(self, track_id, reverb):
        self.instruments[track_id].set_reverb(reverb)

    def set_tempo(self, new_tempo):
        new_time = self.SECONDS_PER_MIN / new_tempo
        self.metronome.setTime(new_time)
        self.tempo = new_tempo

    """getter methods"""
    def get_session(self):
        """Get descriptive MusicPlayer session to restore later"""
        session = Session(self, self.instruments)
        return session

    """getter methods for GUI"""
    def get_reverb(self, track_id):
        return self.instruments[track_id].get_reverb()

    def get_volume(self, track_id):
        return self.instruments[track_id].get_volume()

    def get_global_volume(self):
        return self.global_volume

    def get_tempo(self):
        return self.tempo

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

class Session:
    """Data for saving and loading a composing session"""

    def __init__(self, music_player, instruments):
        """Construct MusicPlayer session for memory"""
        self.tempo = music_player.get_tempo()
        self.instrument_data = []
        for instrument in instruments:
            instrument_data = instrument.get_data()
            self.instrument_data.append(instrument_data)


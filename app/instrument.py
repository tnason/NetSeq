import music_player
from pyo import *

class Instrument:
    """This class holds the sound generator and playback parameters for a track"""

    SECONDS_PER_MIN = 60

    def __init__(self, music_player):
        """ Create generic Instrument

        Arguments:
        music_player: Parent MusicPlayer of this instrument
        """

        self.music_player = music_player
        self.volume = .75
        self.reverb = 0
        self.notes = []

        # Initialize notes array to all zeroes
        for beat_index in range(0, music_player.NUM_BEATS):
            beat_column = []
            for row_index in range(0, music_player.NUM_ROWS):
                beat_column.append(0)
            self.notes.append(beat_column)

    def __del__(self):
        pass

    def get_generator(self):
        return self.generator

    def set_playhead(self):
        pass

    def set_note(self, note):
        beat_index = note.page_index * self.music_player.NUM_COLS +\
                     note.column
        beat_col = self.notes[beat_index]

        print "@@ Altering note at beat ", beat_index, ", row ", note.row

        if note.turn_on == True:
            print "@@ Turn on"
            beat_col[note.row] = 1
        elif note.turn_on == False:
            print "@@ Turn off"
            beat_col[note.row] = 0

    def set_volume(self, volume):
        pass
        
    def set_reverb(self, reverb):
        pass

    def get_volume(self):
        pass

    def get_reverb(self):
        pass

    def get_page(self, page_index):
        """ Get a page of notes with <row, col> indexing """
        start_column = page_index * self.music_player.NUM_COLS
        end_column = start_column + (self.music_player.NUM_COLS - 1)

        page_notes = []
        for row_index in range(0, self.music_player.NUM_ROWS):
            row_notes = []
            for col_index in range(start_column, end_column + 1):
                row_notes.append(self.notes[col_index][row_index])
            page_notes.append(row_notes)
        
        return page_notes

class DrumInstrument(Instrument):
    """This provides functionality for a drum sample instrument"""

    # TODO: finish refining this
    instrument_names = ["Crash", "Tom 2", "Tom 1", "Rim", "Hi Hat 2", "Hi Hat 1", "Snare", "Kick"]
    samples = ["crashedge5.ogg", "hohh_15.ogg", "chh27.ogg"]

    def __init__(self):
        self.generator = None
        pass

    def step(self):
        pass

    def __del__(self):
        pass

class WaveInstrument(Instrument):
    """This provides functionality for a wave instrument"""

    # Frequencis of major scale C4 to C5
    C_FREQUENCIES = [523.25, 493.88, 440.00, 392.00, 349.23, 329.63, 293.66, 261.63]
    BASS = 0
    LEAD = 1
    
    def __init__(self, music_player, wavetype=LEAD):
        """ Create new WaveInstrument

        Arguments
        music_player: Parent MusicPlayer of this instrument
        
        """

        Instrument.__init__(self, music_player)

        if (wavetype == self.BASS):
            table = SquareTable()
            self.frequencies = [(freq / 2) for freq in self.C_FREQUENCIES]
        elif (wavetype == self.LEAD):
            table = CosTable()
            self.frequencies = self.C_FREQUENCIES

        # Generate oscillators for every pitch, feed into mixer
        self.oscillators = []
        self.mixer = Mixer(outs=1)
        for i in range(0, music_player.NUM_ROWS):
            oscillator = Osc(table=table, freq=self.frequencies[i])
            oscillator.stop()
            self.oscillators.append(oscillator)
            self.mixer.addInput(i, oscillator)
            self.mixer.setAmp(i, 0, 1)
        
        # Apply reverb to omixer
        reverb = WGVerb(self.mixer[0], feedback=0.5, cutoff=3500, bal=0)
        
        #use generator.setBal(x) to modify reverb
        self.generator = reverb

    def play_step(self):
        print "@@ Wave instrument step"
        beat_index = self.music_player.beat_index
        beat_col = self.notes[beat_index]

        for row_index in range(0, self.music_player.NUM_ROWS):
            if beat_col[row_index] == 1:
                self.oscillators[row_index].play()
            elif beat_col[row_index] == 0:
                self.oscillators[row_index].stop()

    def __del__(self):
        pass

if __name__ == "__main__":
    instrument = Instrument()

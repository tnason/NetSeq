from music_player import *
from pyo import *

class Instrument:
    """This class holds the sound generator and playback parameters for a track"""

    SECONDS_PER_MIN = 60

    def __init__(self, music_player):
        self.music_player = music_player
        self.volume = .75
        self.reverb = 0
        self.notes = [] #Triple list of notes
        for row in range(0, MusicPlayer.NUM_ROWS):
            col_list = []
            for col in range(0, MusicPlayer.NUM_PAGES*MusicPlayer.NUM_COLS):
                col_list.append(0)
            self.notes.append(col_list)

                    

    def __del__(self):
        pass

    def get_generator(self):
        return self.generator

    def set_playhead(self):
        pass

    def set_note(self, Note):
        pass

    def set_volume(self, volume):
        pass
        
    def set_reverb(self, reverb):
        pass

    def get_volume(self):
        pass

    def get_reverb(self):
        pass

    def get_page(self, page_index):
        pass


class DrumInstrument(Instrument):
    """This provides functionality for a drum sample instrument"""
    def __init__(self):
        self.generator = None
        pass


    def load_beat_full(self):
        pass

    def __del__(self):
        pass

    
    

class WaveInstrument(Instrument):
    """This provides functionality for a wave instrument"""

    FREQUECIES = [523.25, 493.88, 440.00, 392.00, 349.23, 329.63, 293.66, 261.63]
    #C5-C4
    
    def __init__(self, music_player):
        super(WaveInstrument, self).__init__(music_player)
        table = SquareTable()

        beat_time = SECONDS_PER_MIN/self.music_player.tempo
        self.beat = Beat(time=beat_time)

        self.oscillators = []
        self.mixer = Mixer(outs=1)
        for i in range(0, MusicPlayer.NUM_ROWS):
            oscillator = Osc(table=table, freq=FREQUENCIES[i])
            self.oscillators.append(oscillator)
            self.mixer.addInput(i, oscillator)
            self.mixer.setAmp(i, 0, 1)
        
        reverb = WGVerb(self.mixer[0], feedback=0.5, cutoff=3500, bal=0).out()
        
        #use generator.setBal(x) to modify reverb
        self.generator = reverb



    def load_next_beat(self):
        #
        #increment playhead
        pass

    def __del__(self):
        pass

if __name__ == "__main__":
    instr = Instrument()

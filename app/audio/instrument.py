from music_player import Note

class Instrument:
    """This class holds the sound generator and playback parameters for a track"""

    def __init__(self):
        self.volume = .75
        self.reverb = 0
        self.notes = [] #Triple list of notes
        pass

    def __del__(self):
        pass

    def get_generator(self):
        return self.generator

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

    def get_page(self):
        pass

class DrumInstrument(Instrument):
    """This provides functionality for a drum sample instrument"""
    def __init__(self):
        self.generator = None
        pass

    def __del__(self):
        pass

    
    

class WaveInstrument(Instrument):
    """This provides functionality for a wave instrument"""
    def __init__(self):
        self.generator = None
        pass

    def __del__(self):
        pass

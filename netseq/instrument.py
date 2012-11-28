from pyo import Mixer, SndTable, TableRead, WGVerb, SquareTable, CosTable,\
                Osc, Disto, Chorus
import system
import os.path
import sys

class Instrument:
    """This class holds the sound generator and playback parameters for a track"""

    SECONDS_PER_MIN = 60

    def __init__(self, music_player, volume, reverb_mix, notes):
        """ Create generic Instrument

        Arguments:
        music_player: Parent MusicPlayer of this instrument
        """

        self.music_player = music_player
        self.reverb_mix = reverb_mix

        # This field is just for storage. Volume is taken care of in
        # the MusicPlayer's mixer
        self.volume = volume

        # Initialize notes array to all zeroes if no notes input as argument
        if notes == None:
            self.notes = []
            for beat_index in range(0, music_player.NUM_BEATS):
                beat_column = []
                for row_index in range(0, music_player.NUM_ROWS):
                    beat_column.append(0)
                self.notes.append(beat_column)
        else:
            self.notes = notes

        # For generating sound
        self.row_generators = []
        self.reverb_out = None
        self.mixer = Mixer(outs=1)

        # For GUI purposes, override this
        self.names = []

    def __del__(self):
        pass

    def get_generator(self):
        return self.generator

    def get_names(self):
        return self.names

    def pause(self):
        self.mixer.stop()

    def set_note(self, note):
        beat_index = note.page_index * self.music_player.NUM_COLS +\
                     note.column
        beat_col = self.notes[beat_index]
        if note.turn_on == True:
            beat_col[note.row] = 1
        elif note.turn_on == False:
            beat_col[note.row] = 0

    def get_volume(self):
        return self.volume

    def set_volume(self, new_volume):
        self.volume = new_volume

    def get_reverb(self):
        return self.reverb_mix
    
    def set_reverb(self, new_reverb):
        self.reverb_mix = new_reverb    
        self.reverb_out.setBal(new_reverb)

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

    """Abstract methods: override these for your instrument"""
    def play_step(self):
        pass

    def get_data(self):
        pass


class DrumInstrument(Instrument):
    """This provides functionality for a drum sample instrument"""

    sample_files = ["crashedge5.ogg", "large_tom_40-50_1.ogg", 
               "small_tom_40-50_2.ogg", "sidestick24.ogg", "hohh_15.ogg", 
               "chh37.ogg", "snaretop_37.ogg", "kick_22.ogg"]
    sample_amps = [0.2, 1.0, 1.0, 0.3, 0.4, 0.4, 0.3, 0.8]

    def __init__(self, music_player, volume=0.7, reverb_mix=.1, notes=None):
        """ Create new DrumInstrument 

        Arguments:
        music_player: Parent MusicPlayer of this instrument

        """
       
        # Default instrument constructor
        Instrument.__init__(self, music_player, volume, reverb_mix, notes)

        self.names = ["Crash", "Big Tom", "Sm. Tom", "Rim", "HiHat 2", 
                      "HiHat 1", "Snare", "Kick"]

        SOUND_DIR = system.get_sounds_dir()

        self.generator = None
        self.sample_tables = []
        self.generator_cutoff = False        

        for row_index in range(0, music_player.NUM_ROWS):
            file = os.path.join(SOUND_DIR, self.sample_files[row_index])
            sample_table = SndTable(file)
            self.sample_tables.append(sample_table)
            frequency = sample_table.getRate()
            generator = TableRead(table=sample_table, freq=frequency)
            generator.stop()
            self.row_generators.append(generator)
            self.mixer.addInput(row_index, generator)
            self.mixer.setAmp(row_index, 0, self.sample_amps[row_index])

        pre_effect = self.mixer[0]
        post_effect = pre_effect

        # Apply reverb to omixer
        self.reverb_out = WGVerb(post_effect, feedback=0.8, cutoff=3500, 
                                 bal=self.reverb_mix)
        
        #use generator.setBal(x) to modify reverb
        # self.generator = reverb
        self.generator = self.reverb_out

    def __del__(self):
        pass

    def play_step(self):
        """ Walk the instrument through a step of the music """
        #If we were paused, re-enable the mixer
        self.mixer.play()
        beat_index = self.music_player.beat_index
        beat_col = self.notes[beat_index]

        for row_index in range(0, len(self.row_generators)):
            generator = self.row_generators[row_index]
            sample_table = self.sample_tables[row_index]
            sample_dur = sample_table.getDur()
            if beat_col[row_index] == 1:
                generator.stop()
                generator.reset()
                generator.play()

    def get_data(self):
        """Get data for storing and loading this instrument"""
        data = DrumInstrumentData(self.volume, self.reverb_mix, self.notes)
        return data


class WaveInstrument(Instrument):
    """This provides functionality for a wave instrument"""

    # Frequencis of major scale C4 to C5
    C_FREQUENCIES = [523.25, 493.88, 440.00, 392.00, 349.23, 329.63, 293.66, 
                     261.63]
    BASS = 0
    LEAD = 1

    LIMITING_FACTOR = 20
    
    def __init__(self, music_player, wavetype=LEAD, volume=.7, reverb_mix=.1, 
                 notes=None):
        """ Create new WaveInstrument

        Arguments
        music_player: Parent MusicPlayer of this instrument
        
        """

        Instrument.__init__(self, music_player, volume, reverb_mix, notes)

        self.names = ["C", "B", "A", "G", "F", "E", "D", "C"] 

        self.wavetype = wavetype
        if (self.wavetype == self.BASS):
            table = SquareTable()
            self.frequencies = [(freq / 4) for freq in self.C_FREQUENCIES]
        elif (self.wavetype == self.LEAD):
            table = CosTable()
            self.frequencies = self.C_FREQUENCIES

        self.generator_cutoff = True

        # Generate oscillators for every pitch, feed into mixer
        self.oscillators = []
        for i in range(0, music_player.NUM_ROWS):
            oscillator = Osc(table=table, freq=self.frequencies[i])
            oscillator.stop()
            self.row_generators.append(oscillator)
            self.mixer.addInput(i, oscillator)
            self.mixer.setAmp(i, 0, (1.0 / self.LIMITING_FACTOR))
     
        pre_effect = self.mixer[0]

        if (self.wavetype == self.BASS):
            distorted = Disto(pre_effect)
	    volume_reducer = Mixer(outs=1)
	    volume_reducer.addInput(0, distorted)
	    volume_reducer.setAmp(0, 0, 0.3)
	    post_effect = volume_reducer[0]
        elif (self.wavetype == self.LEAD):
            #chorus = Chorus(pre_effect)
            #post_effect = chorus
	    post_effect = pre_effect
        else:
	    post_effect = pre_effect
   
        # Apply reverb to omixer
        self.reverb_out = WGVerb(post_effect, feedback=0.8, cutoff=3500, 
                                 bal=self.reverb_mix)

        #use generator.setBal(x) to modify reverb
        self.generator = self.reverb_out

    def __del__(self):
        pass

    def play_step(self):
        """ Walk the instrument through a step of the music """
        #If we were paused, re-enable the mixer
        self.mixer.play()
        beat_index = self.music_player.beat_index
        beat_col = self.notes[beat_index]

        for row_index in range(0, len(self.row_generators)):
            if beat_col[row_index] == 1:
                self.row_generators[row_index].play()
            elif beat_col[row_index] == 0:
                self.row_generators[row_index].stop()
    
    def get_data(self):
        """Get data for storing and loading this instrument"""
        data = WaveInstrumentData(self.volume, self.reverb_mix, self.notes,
                                  self.wavetype)
        return data;


class InstrumentData:
    """Holds generic instrument data for loading and storing"""

    def __init__(self, volume, reverb_mix, notes):
        """Construct generic Instrument Data"""
        self.volume = volume
        self.reverb_mix = reverb_mix
        self.notes = notes


class WaveInstrumentData(InstrumentData):
    """Holds data for reconstructing WaveInstrument"""
    
    def __init__(self, volume, reverb_mix, notes, wavetype):
        """Construct WaveInstrumentData"""
        InstrumentData.__init__(self, volume, reverb_mix, notes)
        self.wavetype = wavetype


class DrumInstrumentData(InstrumentData):
    """Holds data for reconstructing DrumInstrument"""

    def __init__(self, volume, reverb_mix, notes):
        """Construct DrumInstrumentData"""
        InstrumentData.__init__(self, volume, reverb_mix, notes)


if __name__ == "__main__":
    instrument = Instrument()

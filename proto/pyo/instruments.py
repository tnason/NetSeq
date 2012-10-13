#!/usr/bin/env python
# encoding: utf-8
"""
Creates structures necessary to play back beats over two instrument tracks
and one drum track, and measure the size of these structures.

"""
from pyo import *

# TODO: 
# 1. add scales to this

# Globals
CHANNEL_COUNT = 2

# Initialize server
# TODO: look at format of '=' within arguments
# TODO: choose different audio engine based on platform
# TODO: document the channel playback troubles
# IDEA: can we dump multiple samples into one channel, additatively?
s = Server(sr=44100, nchnls=CHANNEL_COUNT, duplex=0, audio="portaudio").boot()

# Define pre-recorded samples
NUM_DRUM_SAMPLES = 4
drum_samples = ['../../assets/sounds/osdrumkit/kick_22.wav', 
                '../../assets/sounds/osdrumkit/chh37.wav', 
                '../../assets/sounds/osdrumkit/sidestick24.wav', 
                '../../assets/sounds/osdrumkit/snaretop_37.wav']

# Make dummy weight list to avoid dumb Pyo runtime error
WEIGHT_MAX=100
dummy_weight_list = []
for i in range(0, NUM_DRUM_SAMPLES):
    dummy_weight_list.append(WEIGHT_MAX)

# Set preset beats for instruments and drums
inst1_preset = [[16, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1]]
inst2_preset = [[16, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1]]
drum_preset = [[[16, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0]], 
                [[16, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1]], 
                [[16, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0]], 
                [[16, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0]]]

# Generate beats
beat_time = .25

inst1_beat = Beat(time=beat_time)
inst1_beat.setPresets(inst1_preset)
inst1_beat.recall(0)
inst1_beat.play()

inst2_beat = Beat(time=beat_time)
inst2_beat.setPresets(inst2_preset)
inst2_beat.recall(0)
inst2_beat.play()

drum_beat = Beat(time=beat_time, w1=dummy_weight_list, w2=dummy_weight_list,
        w3=dummy_weight_list, poly=4)
drum_beat.setPresets(drum_preset)
drum_beat.recall(0)
drum_beat.play()

# Generate oscillator waveforms
inst1_table = CosTable([(0,0), (100,1), (1000,.25), (8191,0)])
inst1_env = TrigEnv(inst1_beat, table=inst1_table, dur=1, interp=1, mul=1)
inst1_out = Osc(table=inst1_table, freq=240, mul=inst1_env)
# inst1_out.out()

inst2_table = SquareTable()
inst2_env = TrigEnv(inst2_beat, table=inst2_table, dur=1, interp=1, mul=1)
inst2_out = Osc(table=inst2_table, freq=240, mul=inst2_env)
# inst2_out.out()

# Create drum sound generator
# TODO: figure out what's wrong with this table -- sample playback is not as
# expected
drum_table = SndTable(drum_samples)
drum_out = TrigEnv(drum_beat, table=drum_table, dur=drum_beat["dur"], interp=1, mul=1)
drum_mix = Mixer(outs=1, chnls=1)
drum_mix.addInput(0, drum_out)
drum_mix.out()
drum_mix.setAmp(0, 0, .5)

s.gui(locals())

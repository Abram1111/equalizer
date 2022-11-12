
import random 
import streamlit as st

import numpy as np

from scipy.io.wavfile import write
from scipy.signal import find_peaks
import wave
import IPython.display as ipd
import librosa
import librosa.display


import pandas as pd
import altair as alt
import pylab
import os


class variabls :
    points_num =1000
    count=0


def read_audio(audio_file):
    obj = wave.open(audio_file, 'r')
    sample_rate   = obj.getframerate()                           # number of samples per second
    n_samples     = obj.getnframes()                             # total number of samples in the whole audio
    signal_wave   = obj.readframes(-1)                           # amplitude of the sound
    duration      = n_samples / sample_rate                      # duration of the audio file
    sound_info    = pylab.fromstring(signal_wave, 'int16')
    signal_y_axis = np.frombuffer(signal_wave, dtype=np.int16)
    signal_x_axis = np.linspace(0, duration, len(signal_y_axis))
    return signal_x_axis, signal_y_axis, sample_rate,  sound_info
# Plot a Chart
def plot_animation(df):
    lines = alt.Chart(df).mark_line().encode(
        x=alt.X('time', axis=alt.Axis(title='time')),
        y=alt.Y('amplitude', axis=alt.Axis(title='amplitude')),
    ).properties(
        width=500,
        height=250
    )
    return lines





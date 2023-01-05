import random 
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit_vertical_slider  as svs
from scipy.io import wavfile as wav
from scipy.fft import rfft, rfftfreq,irfft,fft, fftshift
import plotly.express as px
import matplotlib as mpl
from scipy import signal
import streamlit.components.v1 as components
import os
import scipy.signal



parent_dir= os.path.dirname(os.path.abspath(__file__))
build_dir=os.path.join(parent_dir,"build")
_vertical_slider= components.declare_component("vertical_slider",path=build_dir)
def vertical_slider (value,step,min=min,max=max,key=None):
  slider_value =_vertical_slider(value=value,step=step,min=min,max=max,key=key,default=value)
  return slider_value
#  ----------------------------------- ECG ---------------------------------------------------
def ECG(df,sliders ):
    list_of_columns = df.columns
    time = (df[list_of_columns[0]])
    magnitude = (df[list_of_columns[1]])
    # Frequency domain representation
    # Inverse fouriour transform for Actual signal
    Magnitude= np.fft.rfft(magnitude)
    Magnitude[0:60] *= sliders[0]
    Magnitude[60:90] *= sliders[1]
    Magnitude[90:250] *= sliders[2]
    Magnitude[250:300] *= sliders[3]
    Magnitude[300:] *= sliders[4] 
    # Do an inverse Fourier transform on the signal
    y_inverse_fourier = np.fft.irfft(Magnitude)
    # store the signal in dataframe 
    data = pd.DataFrame({'time':time, 'amplitude':magnitude }, columns=['time', 'amplitude'])
    data2 = pd.DataFrame({'time':time, 'amplitude':y_inverse_fourier }, columns=['time', 'amplitude'])
    
 
    
    return magnitude , y_inverse_fourier,data, data2

#  ----------------------------------- CREATING SLIDERS ---------------------------------------------------------------
# def creating_sliders(names_list,label):
#     columns = st.columns(10)
#     sliders_values = []
#     sliders = {}

#     for index, tuple in enumerate(names_list): 
      
#         key = f'member{str(index)}'

#         with columns[index]:
#             sliders[f'slidergroup{key}'] = svs.vertical_slider(key=key, default_value=tuple[2], step=0.1, min_value=tuple[0], max_value=tuple[1],slider_color="rgb(255, 75, 75)", thumb_color="rgb(255, 75, 75)")
#             if sliders[f'slidergroup{key}'] == None:
#                 sliders[f'slidergroup{key}'] = tuple[2]
#             sliders_values.append(( sliders[f'slidergroup{key}']))
#             st.write(label[index])
#     return sliders_values

#  --------------------------   FOURIER TRANSFORM FOR  Wave       ----------------------------------------
#  Data is 1-D for 1-channel WAV, or 2-D of shape (Nsamples, Nchannels)
def   fourierTansformWave(audio=[] , sampfreq=440010):
    try:
        audio = audio[:,0]
    except:
        audio = audio[:]


    #  Fourier transform 
    fourier_transform_magnitude = rfft(audio)
    fourier_transform_freq = rfftfreq(len(audio), 1 / sampfreq)
  
    return fourier_transform_magnitude , fourier_transform_freq


# ------------------------------------------  modify_wave   ------------------------------------


def  modify_wave (magnitude=[], numPoints=0 , startIndex=0 , scalerNumber=[], sliders_num = 0):
    for i in range(sliders_num):
        magnitude[startIndex[i]:numPoints[i]+startIndex[i]]*=(scalerNumber[i])
    return magnitude



# --------------------------------------------- bands -------------------------------------------
def bandLength(freq=[]):
    length_band=len(freq)/10
    arr=np.zeros(10)
    for i in range(10):
        arr[i] =int (i*length_band)
        
    return arr  , len(freq)/10  # len(freq)/10 number of piont per band

# ------------------------------------------------------ reconstruction signal -----------------------------------

def reconstruct(signal=[] , sampleRate=0):
        time =np.arange(0,len(signal)/sampleRate,1/sampleRate)
        fig =px.line(x=time,y=signal)
        st.plotly_chart(fig ,use_container_width=True)

def creating_new_slider(label):
    columns = st.columns(len(label))
    sliders_values = []
    for index in range(len(label)):
        with columns[index]:
            slider=vertical_slider(1 , step=1,min= 0 ,max=5 ,key=index)
            sliders_values.append(slider)
            st.write(label[index])
    return sliders_values
#-----------------------------------------------------------------------------------------------------------------
[[[900, 9300]], [[100, 2200], [3950, 7450], [12000, 15000]], [[300, 900], [2600, 20000]], [[1200, 5000]]]
def Vowels(points_per_freq, sliders, frequencies, fourier_frequency):
    vowel = ["sh","M", 'D', 'R']
    for i in range(len(frequencies)):
        # print(frequencies[i][i])
        for j in range(len(frequencies[i])):
            # print(vowel[i],frequencies[i][j][0])
            # print(vowel[i],frequencies[i][j][1])
            signal = fourier_frequency[int(points_per_freq * frequencies[i][j][0]):int(points_per_freq*frequencies[i][j][1])]
            triangle_window = scipy.signal.windows.triang(len(signal))
            
            if sliders[i]<1:
                value = 10**(-100000* triangle_window)    
            else:
                value = 10 ** (((sliders[i]-1) / 10) * triangle_window)
            fourier_frequency[int(points_per_freq * frequencies[i][j][0]):int(points_per_freq*frequencies[i][j][1])] *= value
    return fourier_frequency
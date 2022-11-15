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
    
    # # Create subplot
    # figure, axis= plt.subplots()
    # axis.plot(df_x_axis[50:350],Actual_signal[50:350],label="The Actual Data")
    # axis.plot(df_x_axis[50:350], y_inverse_fourier[50:350],label="After remove arrhythima ")
    # axis.set_xlabel('Time')
    # axis.set_ylabel('Amplitude')
    # st.plotly_chart(figure,use_container_width=True)
    # #  plot spectrogram 
    # fig2= plt.figure(figsize=(9, 3.5))
    # plt.specgram( abs(Actual_signal[:300]))
    # plt.colorbar()
    # st.pyplot(fig2)
    
    return magnitude , y_inverse_fourier,data, data2

#  ----------------------------------- CREATING SLIDERS ---------------------------------------------------------------
def creating_sliders(names_list,label):
    columns = st.columns(10)
    sliders_values = []
    sliders = {}

    for index, tuple in enumerate(names_list): 
      
        key = f'member{str(index)}'

        with columns[index]:
            sliders[f'slidergroup{key}'] = svs.vertical_slider(key=key, default_value=tuple[2], step=0.1, min_value=tuple[0], max_value=tuple[1],slider_color="rgb(255, 75, 75)", thumb_color="rgb(255, 75, 75)")
            if sliders[f'slidergroup{key}'] == None:
                sliders[f'slidergroup{key}'] = tuple[2]
            sliders_values.append(( sliders[f'slidergroup{key}']))
            st.write(label[index])
    return sliders_values

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

def SPectrogram():
    samplfreq, audio = wav.read('convertWave4.wav')  
    magnitude1 , freq_n=fourierTansformWave(audio ,samplfreq) 
    new_sig = irfft(magnitude1)
    return new_sig

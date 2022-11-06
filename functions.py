import random 
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit_vertical_slider  as svs
from scipy.io import wavfile as wav
from scipy.fftpack import fft
from scipy.fft import fft, fftfreq, fftshift
from scipy.fft import irfft
from scipy.fft import rfft, rfftfreq




#  ----------------------------------- FOURIER TRANSFORM FUNCTION ---------------------------------------------------
def fourier_transform(df,sliders ):
    # Getting df x_axis and y_axis
    list_of_columns = df.columns
    df_x_axis = (df[list_of_columns[1]])
    df_y_axis = (df[list_of_columns[3]])
    # Frequency domain representation
    fourier_transform = np.fft.fft(df_y_axis)
    length=(len( fourier_transform ))//2
    frequancy_fourier_transform= fourier_transform[:length]
    fourier_transform[150:]=fourier_transform[150:]*sliders[0]
    # Do an inverse Fourier transform on the signal
    inverse_fourier = np.fft.ifft(fourier_transform)

    # Create subplot
    figure, (axis1,axis2) = plt.subplots(2)
    plt.subplots_adjust(hspace=1)

    # Time domain representation
    axis1.set_title('Fourier transform depicting the frequency components')
    axis1.plot(abs(frequancy_fourier_transform) )
    axis1.set_xlabel('Frequency')
    axis1.set_ylabel('Amplitude')
    axis2.plot(df_x_axis, inverse_fourier,label="Inverse Fourier transform ")
    axis2.plot(df_x_axis,df_y_axis,label="The Actual Data")
    axis2.set_xlabel('Time')
    axis2.set_ylabel('Amplitude')
    st.plotly_chart(figure,use_container_width=True)
    
    return inverse_fourier, fourier_transform ,figure
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
############################ Plotting ######################################################################





#  --------------------------   FOURIER TRANSFORM FOR  Wave       ----------------------------------------
def   fourierTansformWave(audio=[] , sampfreq=440010):
    try:
        audio = audio[: ,1]
    except:
        audio = audio[:]


    #  Fourier transform 
    fourier_transform_magnitude = rfft(audio)
    fourier_transform_freq = rfftfreq(len(audio), 1 / sampfreq)
  
    return fourier_transform_magnitude , fourier_transform_freq


# ------------------------------------------  modify_wave   ------------------------------------

def  modify_wave (magnitude=[], numPoints=0 , startIndex=0 , scalerNumber=1):
    
    for i in range(numPoints):
        magnitude[startIndex+i]=  (magnitude[startIndex+i]*scalerNumber)
    return magnitude

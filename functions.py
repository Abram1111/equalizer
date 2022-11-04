import random 
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import streamlit_vertical_slider  as svs
from scipy.io import wavfile as wav
from scipy.fftpack import fft
from scipy.fft import fft, fftfreq, fftshift



#  ----------------------------------- FOURIER TRANSFORM FUNCTION ---------------------------------------------------
def fourier_transform(df):
    # Getting df x_axis and y_axis
    list_of_columns = df.columns
    df_x_axis = (df[list_of_columns[1]])
    df_y_axis = (df[list_of_columns[3]])
    # Frequency domain representation
    fourier_transform = np.fft.fft(df_y_axis)

    # Do an inverse Fourier transform on the signal
    inverse_fourier = np.fft.ifft(fourier_transform)

    # Create subplot
    figure, axis = plt.subplots()
    plt.subplots_adjust(hspace=1)

    # Frequency domain representation
    axis.set_title('Fourier transform depicting the frequency components')
    axis.plot(df_x_axis, abs(fourier_transform))
    axis.set_xlabel('Frequency')
    axis.set_ylabel('Amplitude')

    st.plotly_chart(figure,use_container_width=True)

    return inverse_fourier, fourier_transform ,figure

#  ----------------------------------- INVERSE FOURIER TRANSFORM FUNCTION ---------------------------------------------------
def fourier_inverse_transform(inverse_fourier,df):
    # Getting df x_axis and y_axis
    list_of_columns = df.columns
    df_x_axis = list(df[list_of_columns[1]])
    df_y_axis = list(df[list_of_columns[3]])

    # Create subplot
    figure, axis = plt.subplots()
    plt.subplots_adjust(hspace=1)

    # Frequency domain representation
    axis.set_title('Inverse Fourier transform depicting the frequency components')
    axis.plot(df_x_axis, inverse_fourier)
    axis.set_xlabel('Frequency')
    axis.set_ylabel('Amplitude')

    fig,ax = plt.subplots()
    ax.set_title('The Actual Data')
    ax.plot(df_x_axis,df_y_axis)
    ax.set_xlabel('Frequency')
    ax.set_ylabel('Amplitude')

    st.plotly_chart(figure,use_container_width=True)
    st.plotly_chart(fig,use_container_width=True)

def wave_ranges(fourier_transform):
    st.write(abs(fourier_transform))

#  ----------------------------------- CREATING SLIDERS ---------------------------------------------------------------
def creating_sliders(names_list,label):
    columns = st.columns(10)
    sliders_values = []
    sliders = {}

    for index, tuple in enumerate(names_list): 
      
        key = f'member{str(index)}'

        with columns[index]:
            sliders[f'slidergroup{key}'] = svs.vertical_slider(key=key, default_value=tuple[2], step=1, min_value=tuple[0], max_value=tuple[1],slider_color="rgb(255, 75, 75)", thumb_color="rgb(255, 75, 75)")
            if sliders[f'slidergroup{key}'] == None:
                sliders[f'slidergroup{key}'] = tuple[2]
            sliders_values.append(( sliders[f'slidergroup{key}']))
            st.write(label[index])
    return sliders_values
############################ Plotting ######################################################################


from tkinter import HIDDEN
import streamlit as st
import streamlit_vertical_slider as svs
import pandas as pd
import functions as fn
from scipy.io.wavfile import write
from scipy.io import wavfile
from scipy.fft import irfft
import numpy as np
# ---------------------- Elements styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# ----------------------- Main Window Elements --------------------------- #
normalIndex=[] 
numofPoints=0
magnitude_n=[]


# ------------------
magnitude=[]
freq=[] 
numPoints_1=0 
startIndex_1=0
numPoints_2=0 
startIndex_2=0
numPoints_3=0 
startIndex_3=0
numPoints_4=0 
startIndex_4=0
samplfreq=0


with st.container():
    upload_col, freq_col = st.columns([1, 4])
    with upload_col:
        file_uploaded = st.file_uploader("")
    with freq_col:
        radio_button = st.radio("", ["Normal", "Music", "Vowels", "Medical","Optional"], horizontal=True)

    if radio_button == "Normal":
        names_list = [(0, 100,0),(0, 100,0),(0, 100,0),(0, 100,0),(0, 100,0),(0, 100,0),(0, 100,0),(0, 100,0),(0, 100,1),(0,100,1)]
        label= ["1kHz","2kHz","3kHz","4kHz","5kHz","6kHz","7kHz","8kHz","9kHz","20kHz"]
        
        if file_uploaded is not None:
            if file_uploaded.type=="audio/wav":
                path=file_uploaded.name   # get path 
                samplfreq , audio = wavfile.read(path)  # read file 
                magnitude_n , freq_n=fn.fourierTansformWave(audio ,samplfreq)   # convert to fft
                normalIndex , numofPoints =fn.bandLength(freq_n)  # get index of slider in how point will change when move slider 


#------------------------------------ MUSIC -----------------------------------------
    elif radio_button == "Music":
        names_list = [(0,100,1),(0,100,1),(0,100,1),(0,100,1)]
        label= ["500Hz","1kHz" , "2kHz" ,"5kHz"]
        
        if file_uploaded is not None:
            if file_uploaded.type=="audio/wav":
                path=file_uploaded.name   # get path 
                samplfreq , audio = wavfile.read(path)  # read file 
                magnitude , freq=fn.fourierTansformWave(audio ,samplfreq)   # convert to fft
                
                points_per_freq = int(len(freq) / (samplfreq / 2) )  # number of points per  frequancy

                numPoints_1=np.abs(0* points_per_freq- 500*points_per_freq)
                numPoints_2=np.abs(500* points_per_freq- 1000*points_per_freq)
                numPoints_3=np.abs(1000* points_per_freq- 2000*points_per_freq) # piano 
                numPoints_4=np.abs(20000* points_per_freq- 5000*points_per_freq)
                startIndex_1=0*points_per_freq
                print(5000*points_per_freq)
                startIndex_2=500* points_per_freq
                startIndex_3=1000*points_per_freq
                startIndex_4=2000* points_per_freq

# ------------------------------------------------- END MUSIC  ----------------------------------


    elif radio_button == "Vowels":
        names_list = [(20,30,25),(20,30,25)]
        label= ["0:100","100:200"]


    elif radio_button == "Medical":
        names_list = [(0,10,1)]
        label= ["0:10"]
        
        
    else:
        names_list = [(20,30,25),(20,30,25)]
        label= ["0:100","100:200"]
  
    sliders =fn.creating_sliders(names_list,label)

    # if file_uploaded:     # ----

    #     df = pd.read_csv(file_uploaded)
    #     inverseFourier, fourierTransform, figure = fn.fourier_transform(df,sliders)
   
   
   
   
# normal 
    if radio_button == "Normal" and len(magnitude_n)>0:
        for i in range(10):
            if i<9: 
                numofPoints=numofPoints/2
            else:
                numofPoints=(numofPoints/2)*9 +numofPoints
                
            magnitude_n=fn.modify_wave(magnitude_n ,int(numofPoints) , int(normalIndex[i]/2),sliders[i]*100) 

        
        
        new_sig = irfft(magnitude_n)
        norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
        write("singnal.wav", samplfreq, norm_new_sig)
        st.audio("singnal.wav" )
        
        #  to plot reconstuctoin 
        sampleRate , sound = samplfreq , audio = wavfile.read("singnal.wav")
        fn.reconstruct(sound , sampleRate)   
    
#  music 
    if radio_button == "Music" and len(magnitude)>10:
        magnitude=fn.modify_wave(magnitude , numPoints_1 , startIndex_1 , sliders[0]*10) 
        magnitude=fn.modify_wave(magnitude , numPoints_2 , startIndex_2 , sliders[1]*10) 
        magnitude=fn.modify_wave(magnitude , numPoints_3 , startIndex_3 , sliders[2]*10) 
        magnitude=fn.modify_wave(magnitude , numPoints_4 , startIndex_4 , sliders[3]*10) 
        
        
        new_sig = irfft(magnitude)
        norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
        write("convertWave4.wav", samplfreq, norm_new_sig)
        st.audio("convertWave4.wav" )
        
        #  to plot reconstuctoin 
        sampleRate , sound = samplfreq , audio = wavfile.read("convertWave4.wav")
        fn.reconstruct(sound , sampleRate)
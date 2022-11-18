from tkinter import HIDDEN
import streamlit as st
import streamlit_vertical_slider as svs
import pandas as pd
import functions as fn
from scipy.io.wavfile import write
from scipy.io import wavfile
from scipy.fft import irfft
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
import plotly_express as px
import IPython.display as ipd
import librosa
import altair as alt
import animation as animation
import time
import plotly.graph_objects as go
import soundfile as sf
#-------------------------- Elements styling ----------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# ----------------------- Main Window Elements --------------------------- #

normalIndex=[] 
numofPoints=0
magnitude_n=[]

# sliders = []
# ------------------
magnitude=[]
freq=[] 
numpoints = []
startIndex =[]
samplfreq=0
lines1=any
optional =  False
# -------------------------------------------------------------------------------------------------------------#
file_uploaded = st.sidebar.file_uploader("")

radio_button = st.sidebar.radio("", ["Normal", "Music", "Vowels", "Medical","Optional"], horizontal=False)

before_col,after_col=st.columns(2)
if "size" not in st.session_state:
    st.session_state['size'] = 0
if "counter" not in st.session_state:
    st.session_state['counter'] = 0
if "btn_state" not in st.session_state:
    st.session_state['btn_state'] = 0
if file_uploaded==None:
    # welcome_text = '<p class="page_titel", style="font-family:Arial">Please upload file </p>'
    # st.markdown(welcome_text, unsafe_allow_html=True)
    name="singnal.wav"
    type="audio/wav"
    


if (radio_button == "Music" or radio_button == "Normal" or radio_button == "Vowels" or radio_button =="Optional"):
    if file_uploaded !=None:
            name=file_uploaded.name
            type = file_uploaded.type
    if type=="audio/wav":
        signal_x_axis_before, signal_y_axis_before, sample_rate_before ,sound_info_before = animation.read_audio(name)
        df = pd.DataFrame({'time': signal_x_axis_before[::500], 'amplitude': signal_y_axis_before[:: 500]}, columns=['time', 'amplitude'])
        lines = alt.Chart(df).mark_line().encode( x=alt.X('time', axis=alt.Axis(title='time')),
                                                y=alt.Y('amplitude', axis=alt.Axis(title='amplitude'))).properties(width=500,height=200)
        # st.write(file_uploaded)
        samplfreq, audio = wavfile.read(name)  
        magnitude , freq=fn.fourierTansformWave(audio ,samplfreq)  
        points_per_freq = np.ceil(len(freq) / (samplfreq / 2) )  # number of points per  frequancy 
        points_per_freq = int(points_per_freq) # convert to fft
        if radio_button == "Normal":
            label= ["{}Hz".format(500),"{}Hz".format(1000),"{}Hz".format(1500),"{}Hz".format(2000),"{}Hz".format(2500),"{}Hz".format(3000),"{}Hz".format(3500),"{}Hz".format(4000),"{}Hz".format(4500),"{}Hz".format(5000)]
            # read file          
            sliders =fn.creating_new_slider(label)
            normalIndex , numofPoints =fn.bandLength(freq)  # get index of slider in how point will change when move slider 
            for i in range(10):
                if i<9: 
                    numpoints.append(int(numofPoints/2))
                else:
                    numofPoints=(numofPoints/2)*9 +numofPoints
                    numpoints.append(int(numofPoints))
                startIndex.append(int(normalIndex[i]/2))
            print("This is ",numofPoints)
            # numpoints = int(numofPoints)
#------------------------------------ MUSIC -----------------------------------------

        elif radio_button == "Music":
            
            # drums from 0 to  500 hz 
            #  piano from 500 to 2000 
            #  guiter from  200 to  7000 
            label= [" Drums","piano" ,"guitar"]
            sliders =fn.creating_new_slider(label)
            frequencies = [0, 500,  2000, 7000]
            for i in range(len(label)):
                    numpoints.insert(i,np.abs(frequencies[i] * points_per_freq - frequencies[i+1] * points_per_freq))
                    startIndex.insert(i,frequencies[i] * points_per_freq)
 
# ------------------------------------------------- END MUSIC  --------------------------------

# -------------------------------------------------  Vowels  ----------------------------------

        elif radio_button == "Vowels":
            label= ["sh","M", 'D', 'R']
            sliders =fn.creating_new_slider(label)
            frequencies = [[[900, 9300]], [[100, 2200], [3950, 7450], [12000, 15000]], [[100, 900], [1800, 20000]], [[1200, 500]]]
            # startIndex, numpoints = fn.get_data(samplfreq,freq,frequencies,len(label))
            print(frequencies[1][0])
# ------------------------------------------------- END Vowels  ---------------------------------
        elif radio_button=="Optional":      
            label=["wolf", "bird"]
            sliders =fn.creating_new_slider(label)
            frequencies=[400,2500,20000]
            for i in range(len(label)):
                    numpoints.insert(i,np.abs(frequencies[i] * points_per_freq - frequencies[i+1] * points_per_freq))
                    startIndex.insert(i,frequencies[i] * points_per_freq)
            
        magnitude_spactro=magnitude
        spectrogramOrigin = irfft(magnitude_spactro)
        # plot spactro (before)
        fig_befor_spacrto = plt.figure(figsize=(5, 1.5))
        plt.specgram(spectrogramOrigin, Fs=samplfreq, vmin=-20, vmax=50)
        plt.colorbar()
        
        #end plot spactro (before)
        if(radio_button == "Vowels"):
            magnitude = fn.Vowels(points_per_freq, sliders, frequencies, magnitude)
        else:
            magnitude=fn.modify_wave(magnitude , numpoints , startIndex , sliders, len(label))
        new_sig = irfft(magnitude)
        norm_new_sig = np.int16(new_sig * (32767 / new_sig.max()))
        write("convertWave4.wav", samplfreq, norm_new_sig)
        signal_x_axis_after, signal_y_axis_after, sample_rate_after ,sound_info_after = animation.read_audio("convertWave4.wav")    # Read Audio File
        df1 = pd.DataFrame({'time': signal_x_axis_after[::500], 'amplitude': signal_y_axis_after[:: 500]}, columns=['time', 'amplitude'])
        lines1 = alt.Chart(df1).mark_line().encode( x=alt.X('time', axis=alt.Axis(title='time')),
                                                y=alt.Y('amplitude', axis=alt.Axis(title='amplitude'))).properties(width=500,height=200)

        fig2 = plt.figure(figsize=(5, 1.5))
        plt.specgram(new_sig, Fs=samplfreq, vmin=-20, vmax=50)
        plt.colorbar()
        # Plot Animation
        
        with before_col:
            before_text = '<p class="before", style="font-family:Arial"> before </p>'
            st.markdown(before_text, unsafe_allow_html=True)
            st.audio(name)
            line_plot_before = st.altair_chart(lines)
            st.pyplot(fig_befor_spacrto)
        with after_col:
            after_text = '<p class="after", style="font-family:Arial"> after </p>'
            st.markdown(after_text, unsafe_allow_html=True)
            st.audio("convertWave4.wav" )
            line_plot_after= st.altair_chart(lines1)
            st.pyplot(fig2)
        start_btn_col,reset_btn_col =st.sidebar.columns(2)
        with start_btn_col:
            placeholder=st.empty()
            start_btn =  placeholder.button('Start')
        with reset_btn_col:
            reset_btn =st.button('reset')
        N = df.shape[0]  # number of elements in the dataframe
        burst = int(len(df1)/4)       # number of elements (months) to add to the plot
        size = burst     # size of the current dataset 
        if start_btn  and st.session_state["btn_state"]==0:
            st.session_state['btn_state']=1
            placeholder.empty()
            start_btn=placeholder.button('Pause')
            for i in range(st.session_state["size"]+burst, N - burst):
                i=st.session_state['counter']
                step_df  = df.iloc[i:st.session_state['size']]
                step_df1 = df1.iloc[i:st.session_state['size']]

                lines  = animation.plot_animation(step_df)
                lines1 = animation.plot_animation(step_df1)


                line_plot_befor  = line_plot_before.altair_chart(lines)
                line_plot_after= line_plot_after.altair_chart(lines1)

                st.session_state['size'] = i + burst
                if st.session_state['size'] >= N:
                    st.session_state['size'] = N - 1
                time.sleep(.00000000001)
                st.session_state['counter'] += 1
        
        if  st.session_state["btn_state"]==1:
            st.session_state["btn_state"]=0
            step_df  = df.iloc[st.session_state['counter']:st.session_state['size']]
            step_df1 = df1.iloc[st.session_state['counter']:st.session_state['size']]
            lines  = animation.plot_animation(step_df)
            lines1 = animation.plot_animation(step_df1)
            line_plot_befor  = line_plot_before.altair_chart(lines)
            line_plot_after= line_plot_after.altair_chart(lines1) 
        if reset_btn_col:
            st.session_state['size'] =0
            st.session_state['counter'] = 0
            st.session_state["btn_state"]=0
    else:
        error_text = '<p class="error", style="font-family:Arial"> The format is invalid, please make sure that the file is in wav format </p>'
        st.markdown(error_text, unsafe_allow_html=True)
# ----------------------- Medical ------------------------------------------------------- # 
elif radio_button == "Medical":
    label= ["Bradycardia","Normal","Techycardia","Atrial Flutter","Atrial"]
    if(file_uploaded.type == "text/csv"):
        sliders =fn.creating_new_slider(label)
        df = pd.read_csv(file_uploaded)
        Actual_signal, y_inverse_fourier,data, data2 = fn.ECG(df,sliders)
        
        lines = alt.Chart(data).mark_line().encode( x=alt.X('time', axis=alt.Axis(title='time')),
                                                y=alt.Y('amplitude', axis=alt.Axis(title='amplitude'))).properties(width=500,height=200)
        lines_1 = alt.Chart(data2).mark_line().encode( x=alt.X('time', axis=alt.Axis(title='time')),
                                                y=alt.Y('amplitude', axis=alt.Axis(title='amplitude'))).properties(width=500,height=200)
        figure1= plt.figure(figsize=(4,1.5))
        plt.specgram( abs(Actual_signal[:300]))
        plt.colorbar()
        figure2= plt.figure(figsize=(4,1.5))
        plt.specgram( abs(y_inverse_fourier[:300]))
        plt.colorbar()
        start_btn_col ,reset_btn_col =st.sidebar.columns(2)
        with start_btn_col:
            placeholder=st.empty()
            start_btn =  placeholder.button('Start')
        with reset_btn_col:
            reset_btn =st.button('reset')
        # Plot Animation
        # before_col,after_col=st.columns(2)
        with before_col:
            before_text = '<p class="before", style="font-family:Arial"> before </p>'
            st.markdown(before_text, unsafe_allow_html=True)
            line_plot_before = st.altair_chart(lines)
            st.pyplot(figure1)
        with after_col:
            after_text = '<p class="after", style="font-family:Arial"> after </p>'
            st.markdown(after_text, unsafe_allow_html=True)
            line_plot_after= st.altair_chart(lines_1)
            st.pyplot(figure2)
            
        N = data.shape[0] # number of elements in the dataframe
        burst = int(len(data2)/4)       # number of elements (months) to add to the plot
        size = burst      # size of the current dataset 
        if start_btn  and st.session_state["btn_state"]==0:
            st.session_state['btn_state']=1
            placeholder.empty()
            start_btn=placeholder.button('Pause')
            for i in range(1, N):
                i=st.session_state['counter']
                step_df  = data.iloc[0:st.session_state['size']]
                step_df1 = data2.iloc[0:st.session_state['size']]

                lines  = animation.plot_animation(step_df)
                lines1 = animation.plot_animation(step_df1)


                line_plot_befor  = line_plot_before.altair_chart(lines)
                line_plot_after= line_plot_after.altair_chart(lines1)

                st.session_state['size'] = i + burst
                if st.session_state['size'] >= N:
                    st.session_state['size'] = N - 1
                time.sleep(.00000000001)
                st.session_state['counter'] += 1
        if  st.session_state["btn_state"]==1:
            st.session_state["btn_state"]=0
            step_df  = data.iloc[0:st.session_state['size']]
            step_df1 = data2.iloc[0:st.session_state['size']]
            lines  = animation.plot_animation(step_df)
            lines1 = animation.plot_animation(step_df1)
            line_plot_befor  = line_plot_before.altair_chart(lines)
            line_plot_after= line_plot_after.altair_chart(lines1)             
        if reset_btn_col:
            st.session_state['size'] =0
            st.session_state['counter'] = 0
            st.session_state["btn_state"]=0
    else:
        error_text = '<p class="error", style="font-family:Arial"> The format is invalid, please make sure that the file is in CSV format </p>'
        st.markdown(error_text, unsafe_allow_html=True)
        
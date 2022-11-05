from tkinter import HIDDEN
import streamlit as st
import streamlit_vertical_slider as svs
import pandas as pd
import functions as fn
# ---------------------- Elements styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# ----------------------- Main Window Elements --------------------------- #
with st.container():
    upload_col, freq_col = st.columns([1, 4])
    with upload_col:
        file_uploaded = st.file_uploader("")
    with freq_col:
        radio_button = st.radio("", ["Normal", "Music", "Vowels", "Medical","Optional"], horizontal=True)

    if radio_button == "Normal":
        names_list = [(0, 10,2),(10,20,15),(20,30,25),(20,30,25),(20,30,25),(20,30,25),(20,30,25),(20,30,25),(20,30,25),(20,30,25)]
        label= ["0:100","100:200","200:300","0:100","100:200","200:300","0:100","100:200","200:300","200:300"]


    elif radio_button == "Music":
        names_list = [(20,30,25),(20,30,25)]
        label= ["0:100","100:200"]


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

    if file_uploaded:

        df = pd.read_csv(file_uploaded)
        inverseFourier, fourierTransform, figure = fn.fourier_transform(df,sliders)
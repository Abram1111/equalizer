from tkinter import HIDDEN
import streamlit as st
import streamlit_vertical_slider as svs
import pandas as pd
# ---------------------- Elements styling -------------------------------- #
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# ----------------------- Main Window Elements --------------------------- #
with st.container():
    upload_col, freq_col = st.columns([
        1, 4])
    with upload_col:
        file_uploaded = st.file_uploader("")
    with freq_col:
        normal_freq = st.radio("", [
                               "normal ", "music ", "vowels", "medical"], horizontal=True)
   
groups = [('2021-01-01',0),
            ('2021-01-02',0),
            ('2021-01-03',0),
            ('2021-01-04',0),
            ('2021-01-05',0),
            ('2021-01-06',0),
            ('2021-01-07',0),
            ('2021-01-08',0),
            ('2021-01-09',0),
            ('2021-01-10',0)
            ]
lables=["rang1","rang2","rang3","rang4","rang5","rang6","rang7","rang8","rang9","rang10"]
boundary = int(50)
adjusted_data = []
sliders = {}
columns = st.columns(len(groups))
for idx, i in enumerate(groups):
    min_value = i[1] - boundary
    max_value = i[1] + boundary
    key = f'member{str(idx)}'
    with columns[idx]:
        sliders[f'slider_group_{key}'] = svs.vertical_slider(key=key, default_value=i[1], step=1, min_value=min_value, max_value=max_value,slider_color="rgb(255, 75, 75)", thumb_color="rgb(255, 75, 75)")
        if sliders[f'slider_group_{key}'] == None:
            sliders[f'slider_group_{key}']  = i[1]
        adjusted_data.append((i[0],sliders[f'slider_group_{key}'] ))
        st.write(lables[idx])
df = pd.DataFrame(adjusted_data, columns=['Date','Value'])
st.line_chart(df, x='Date', y='Value')

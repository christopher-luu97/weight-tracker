import streamlit as st
import pandas as pd
import numpy as np
import plotly as ply
import datetime

# Page setting
st.set_page_config( page_title="Daily Weight Tracker",
                    page_icon=":date:",
                    layout = "wide",)
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
# Data
data = pd.read_csv("./output_data/test.csv")
date = data.iloc[:, 1:]
data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
data['Date'] = data['Date'].dt.date

# Sidebar for filters
st.sidebar.header("Please Filter Here:")

# Slider for filters
# https://discuss.streamlit.io/t/datetime-slider/163/12
cols1, _ = st.sidebar.columns((10,2))
format = 'MMM DD, YYYY'
#start_date = datetime.datetime.strptime(data['Date'][0],"%Y-%M-%d").date()
start_date = data['Date'][0]
end_date = datetime.date.today()
max_dates = end_date - start_date
slider = cols1.slider('Select date', min_value = start_date, value = end_date, 
                                        max_value=end_date, format=format)
st.sidebar.table(pd.DataFrame([[start_date, slider, end_date]],
            columns = ['start', 'selected', 'end'],
            index=['Date']))

main_table = st.dataframe(data[data['Date']<=slider])

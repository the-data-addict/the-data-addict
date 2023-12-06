import pandas as pd
import streamlit as st
import numpy as np


st.title(
    "Uber Pick ups in NYC"
)

Date_Column = 'date/time'
Data_Url = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache_data(persist=True)
def load(nrows):
    data = pd.read_csv(Data_Url, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[Date_Column] = pd.to_datetime(data[Date_Column])
    return data


# %%
data_load_state = st.text('Loading data...')
data = load(10000)
data_load_state.text("Done! (using st.cache_data)")

st.subheader('Raw Data')
st.write(data)

st.subheader('Number of pickups by hour')

hist_values = np.histogram(
    data[Date_Column].dt.hour,bins=24, range = (0,24)) [0]
st.bar_chart(hist_values)


hour_filter = 17
filtered_date = data[data[Date_Column].dt.hour == hour_filter]
st.subheader(f'Map of all pickups at {hour_filter}:00')
st.map(filtered_date)

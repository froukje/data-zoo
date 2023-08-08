import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.buy_me_a_coffee import button
import streamlit_analytics
import pandas as pd
import numpy as np
import seaborn as sns
import config
streamlit_analytics.start_tracking()

st.set_page_config(page_title="data app for data science and machine learning")

DATA_URL = 'data/water_potability.csv'

## sidebar
add_logo("images/datenraum_klein.png", height=50)
st.sidebar.markdown("If you like this app, tell your friends and consider giving me a :star: Thank you! :yellow_heart:")

## main
st.image("images/datenraum_writing.png")

st.markdown("### ⚠️  THIS APP IS UNDER DEVELOPMENT! ⚠️ ")

st.markdown("# Analyse Your Data with Datenraum!")
st.markdown("### Upload your own data, visualize it, make statistical analysis and Machine Learning!")

uploaded_file = st.file_uploader("Choose a file")
st.markdown('Supported file types: csv')
if uploaded_file is None:
    df = pd.read_csv(DATA_URL)

st.markdown('---')
st.markdown("# Use Provided Data")
st.markdown("To explore the possibilites, you can also use the data provided by default. The data loaded by default can be used to classify the water quality in 'potable' and 'not potable'. It contains several parameters that characterize water quality and a column that says whether the water is potable or not. The data is downloaded from [kaggle](https://www.kaggle.com/datasets/adityakadiwal/water-potability). You can find a more detailed description there. It describes a binary classification problem.")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
st.session_state["dataframe"] = df

# show Dataframe
cm = sns.light_palette(config.COLOR, as_cmap=True)
properties = {"border": "2px solid gray"}
s = df.style.format(precision=3)\
      .highlight_null(color='red')\
      .background_gradient(cmap=cm)\
      .bar(align="mid", color=["red", "lightgreen"])\
      .set_properties(**properties)
st.dataframe(s)


button(username="pumaline", floating=False, width=221)
streamlit_analytics.stop_tracking()

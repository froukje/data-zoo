import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns

st.set_page_config(page_title="data app for visualisation and machine learning")
#st.header("Datenraum")
#st.subheader("Data app for Visualisation and Machine Learning")

#DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
#            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')
DATA_URL = 'data/water_potability.csv'

st.sidebar.markdown("# Home")

st.markdown("# Datenraum")

st.markdown("### ⚠️  THIS PAGE IS UNDER DEVELOPMENT! ⚠️ ")

st.markdown("### Easy explore your data with Datenraum!")
st.markdown("Upload your own data (.csv-format), visualize it, make statistical analysis and Machine Learning!")
st.markdown("To explore the possibilites, you can use the data provided by default. The data loaded by default describes several paramters of water quality and a column that says whether the water quality is good or bad. The data is downloaded from [kaggle](https://www.kaggle.com/datasets/adityakadiwal/water-potability). You can find a more detailed description there. This data describes a classification problem.")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    df = pd.read_csv(DATA_URL)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

st.session_state["dataframe"] = df

# show Dataframe
cm = sns.light_palette("green", as_cmap=True)
properties = {"border": "2px solid gray"}
s = df.style.format(precision=3)\
      .highlight_null(color='red')\
      .background_gradient(cmap=cm)\
      .bar(align="mid", color=["red", "lightgreen"])\
      .set_properties(**properties)
st.dataframe(s) 

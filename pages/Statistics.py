import streamlit as st
import pandas as pd

if "dataframe" in st.session_state:
    df=st.session_state["dataframe"]

st.markdown("# Statistics")
st.sidebar.markdown("# Statistics")

if st.sidebar.checkbox('Data Types'):
    st.markdown("### Data Types")
    st.write(df.dtypes)
if st.sidebar.checkbox('Basic Statistics'):
    st.markdown('### Basic Statistics')
    st.write(df.describe())
if st.sidebar.checkbox('Missing Values'):
    st.markdown("### Number of missing values in each column")
    st.write(df.isna().sum())

import streamlit as st
from streamlit_extras.app_logo import add_logo
from streamlit_extras.buy_me_a_coffee import button
import streamlit_analytics
from utils_viz import (line, 
                   scatter, 
                   hist, 
                   hist_multiple,
                   ridgeline)
streamlit_analytics.start_tracking()

if "dataframe" in st.session_state:
    df=st.session_state["dataframe"]

## main
st.markdown("# Data Exploration")

st.markdown("### What would you like to plot?")
st.markdown("Select from the options in the sidebar to plot your data.")

st.markdown("---")


## sidebar
add_logo("images/datenraum_klein.png", height=50)

if st.sidebar.checkbox('Show Dataframe'):
    st.dataframe(df)

st.sidebar.markdown("**Statistics**")
statistics = ['', 'Data Types', 'Basic Statistics', 'Missing Values']
show_stats = st.sidebar.selectbox(
                'Select Statistics',
                statistics)

plot_type_single = ['','Linechart', 'Scatterplot', 'Histogram']
# boxplot 
# https://datavizcatalogue.com/
# https://www.data-to-viz.com/

plot_type_multiple = ['', 'Histogram', 'Ridgeline']
st.sidebar.markdown("**Plot one or two Variables**")
s_plot = st.sidebar.selectbox(
            'Select a Plot Type for a single plot',
            plot_type_single)
st.sidebar.markdown("**Plot Multiple Variables**")
m_plot = st.sidebar.selectbox(
        'Select a Plot Type for multiple plots',
            plot_type_multiple)

st.sidebar.markdown("If you like this app, tell your friends and consider giving me a :star: Thank you! :yellow_heart:")

## main

### statistics
if show_stats=='Data Types':
    st.write(df.dtypes)
if show_stats=='Basic Statistics':
    st.write(df.describe())
if show_stats=='Missing Values':
    st.write(df.isna().sum())

### plots
if s_plot=='Linechart':
    line(df)
if s_plot=='Scatterplot':
    st.markdown("Draw a scatterplot of two columns of your dataframe.")
    scatter(df)
if s_plot=='Histogram':
    st.markdown("Draw a histogram of one of the columns of your dataframe. You can choose the number of bins between 5 and 100.")
    hist(df)


if m_plot=='Histogram':
    hist_multiple(df)
if m_plot=='Ridgeline':
    ridgeline(df)

with st.sidebar:
    button(username="pumaline", floating=False, width=221)
streamlit_analytics.stop_tracking()

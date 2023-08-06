import streamlit as st
from utils_viz import (line, 
                   scatter, 
                   hist, 
                   ridgeline)

st.sidebar.markdown("# Visualization")
st.markdown("# Visualization")

if "dataframe" in st.session_state:
    df=st.session_state["dataframe"]

st.markdown("### What would you like to plot?")
st.markdown("Select from the options in the sidebar to plot your data.")
st.markdown("---")
if st.sidebar.checkbox('Show Dataframe'):
    st.dataframe(df)

plot_type_single = ['','Linechart', 'Scatterplot', 'Histogram']
# boxplot 
# https://datavizcatalogue.com/
# https://www.data-to-viz.com/

plot_type_multiple = ['','Ridgeline']

st.sidebar.markdown("**Plot Single Column**")
s_plot = st.sidebar.selectbox(
            'Select a Plot Type',
            plot_type_single)

st.sidebar.markdown("**Plot Multiple Columns**")
m_plot = st.sidebar.selectbox(
            'Select a Plot Type',
            plot_type_multiple)

if s_plot=='Linechart':
    line(df)
if s_plot=='Scatterplot':
    st.markdown("Draw a scatterplot of two columns of your dataframe.")
    scatter(df)
if s_plot=='Histogram':
    st.markdown("Draw a histogram of one of the columns of your dataframe. You can choose the number of bins between 5 and 100.")
    hist(df)


if m_plot=='Ridgeline':
    ridgeline(df)

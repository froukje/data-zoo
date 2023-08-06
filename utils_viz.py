import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import joypy
import config

def line(df):
    col = st.selectbox(
        'Select a column to draw a linechart',
        df.columns)
    y = df[col].values
    try:
        fig, ax = plt.subplots()
        ax.plot(y, color=config.COLOR) 
        st.pyplot(fig)
    except:
        st.write("It is not possible to draw a linechart with the selected column")

def scatter(df):
    x_col = st.selectbox(
            'Select a column for the x-axis',
            df.columns)
    y_col = st.selectbox(
            'Select a column for the y-axis',
            df.columns)
    x = df[x_col].values
    y = df[y_col].values
    try: 
        fig, ax = plt.subplots()
        ax.scatter(x, y, s=5, color=config.COLOR)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        st.pyplot(fig)
    except:
        st.write("It is not possible to draw a scatterplot with the selected variables.")

def hist(df):
    bins = st.slider('nr. of bins', min_value=5, max_value=100, step=5, value=20, help="select the nr. of bins for the histogram")
    col = st.selectbox(
            'Select a column to draw a histogram',
            df.columns)
    try:
        fig, ax = plt.subplots()
        ax.hist(df[col], bins=bins, color=config.COLOR)
        #ax.xticks(rotate=90)
        st.pyplot(fig)
    except:
        st.write("It is not possible tp draw a histogram with the selected variable")

def ridgeline(df):
    try:
        # https://python-charts.com/distribution/ridgeline-plot-matplotlib/#:~:text=84%20Next-,Ridgeline%20plots%20with%20the%20joyplot%20function,variables%20of%20the%20data%20frame.
        fig, ax = joypy.joyplot(df)
        st.pyplot(fig)
    except:
        st.write("It is not possible to draw a Ridgeline plot")



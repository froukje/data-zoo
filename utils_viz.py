import streamlit as st
import streamlit.components.v1 as components
import matplotlib.pyplot as plt
import numpy as np
import mpld3
import seaborn as sns
import joypy
import config
import explanations

def select_vars(df, type='line'):
    '''
    slect valraibles for a single plot
    ::in parameters:: dataframe
    ::returns:: 
        x - dataframe column for x axis
        y - dataframe column for y axis
        sep - dataframe column to group plot
    '''
    col_y = st.selectbox(
        'Select a column for the y axis',
        df.columns)
    y = col_y
    
    if type=='line':
        x_list = ['index']
        x_list.extend(list(set(df.columns.to_list()) - set(col_y)))
    if type=='scatter':
        x_list = df.columns
    if type=='hist':
        x_list = [None]
        x_list.extend(df.columns.to_list())

    col_x = st.selectbox(
        'Select a column for the x axis',
        x_list)

    sns.set_palette(config.PALETTE)
    if col_x == 'index':
        x = df.index
    else:
        x = col_x

    sep_list = [None]
    if col_x:
        sep_list.extend(list(set(df.columns.to_list()) - set(col_y) - set(col_x)))
    else:
        sep_list.extend(list(set(df.columns.to_list()) - set(col_y)))

    sep = st.selectbox(
        'Select a variable to group data',
        sep_list)
    return x, y, sep 

def select_vars_for_multiple_plots(df, type_='group'):
    '''
    select variables to plot
    '''
    data_cols = []
    for col in df.columns:
        if st.checkbox(col):
            data_cols.append(col)

    x_list = ['index']
    x_list.extend(list(set(df.columns.to_list()) - set(data_cols)))
    if type_=='group':
        col_x = st.selectbox(
            'Select a variable to group data',
            x_list)
        if col_x == 'index':
            by = None
        else:
            by = col_x

        return data_cols, by
    if type_=='no_group':
        return data_cols

def line(df):
    '''
    draw a linechart 
    ::in param:: dataframe
    '''
    if st.checkbox("Show explanation for 'Linechart'"):
        st.markdown(explanations.LINECHART)
    x, y, sep = select_vars(df, type='line')

    try:
        fig, ax = plt.subplots()
        sns.set_palette(config.PALETTE)
        sns.lineplot(data=df, y=y, x=x, hue=sep, ax=ax)
        fig_html = mpld3.fig_to_html(fig)
        components.html(fig_html, height=600)
    except:
        st.write("It is not possible to draw a linechart with the selected column")

def scatter(df):
    '''
    plot a scatterplot of two selected variables grouped by an optinal third variable.
    ::in param:: dataframe
    '''
    if st.checkbox("Show explanation for 'Scatterplot'"):
        st.markdown(explanations.SCATTERPLOT)
    
    x, y, sep = select_vars(df, type='scatter')

    try: 
        fig, ax = plt.subplots()
        sns.set_palette(config.PALETTE)
        sns.scatterplot(data=df, x=x, y=y, hue=sep, ax=ax)
        fig_html = mpld3.fig_to_html(fig)
        components.html(fig_html, height=600)
    except:
        st.write("It is not possible to draw a scatterplot with the selected variables.")

def hist(df):
    '''
    plot a histogram of.
    ::in param:: dataframe
    '''
    if st.checkbox("Show explanation for 'Histogram'"):
        st.markdown(explanations.HISTOGRAM)

    x, y, sep = select_vars(df, type='hist')

    bins = st.slider('nr. of bins', min_value=5, max_value=100, step=5, value=20, help="select the nr. of bins for the histogram")
    try:
        fig, ax = plt.subplots()
        sns.set_palette(config.PALETTE)
        sns.histplot(data=df, x=x, y=y, hue=sep, bins=bins)
        fig_html = mpld3.fig_to_html(fig)
        components.html(fig_html, height=600)

    except:
        st.write("It is not possible tp draw a histogram with the selected variable")

def ridgeline(df):
    '''
    ridgeline plot
    '''
    if st.checkbox("Show explanation for 'Ridgeline Plot'"):
        st.markdown(explanations.RIDGELINE)
    
    st.markdown("Choose the variables you would like to plot")
    data, by = select_vars_for_multiple_plots(df, type_='group')
    try:
        # https://python-charts.com/distribution/ridgeline-plot-matplotlib/#:~:text=84%20Next-,Ridgeline%20plots%20with%20the%20joyplot%20function,variables%20of%20the%20data%20frame.
        fig, ax = joypy.joyplot(df, by=by, column=data)
        fig_html = mpld3.fig_to_html(fig)
        components.html(fig_html, height=600)

    except:
        st.write("It is not possible to draw a Ridgeline plot")

def hist_multiple(df):
    '''
    plot histograms of multiple variables in df
    ::in params:: dataframe
    '''
    if st.checkbox("Show explanation for 'Historam'"):
        st.markdown(explanations.HISTOGRAM)
    
    data = select_vars_for_multiple_plots(df, type_='no_group')
    nr_vars = df[data].values.shape[1]
    st.markdown('---')

    if st.checkbox('All in one plot'):
        try:
            fig, ax = plt.subplots()
            for i in range(nr_vars):
                ax.hist(df[data].values[:, i], alpha=1/nr_vars)
                fig_html = mpld3.fig_to_html(fig)
                components.html(fig_html, height=600)
        except:
            st.write("It is not possible tp draw a histogram with the selected variable")

    if st.checkbox('Multiple plots'):
        rows = np.ceil(nr_vars/3)
        try:
            fig, axes = plt.suplots(rows, 3)
            for i, ax in enumertae(axes.flatten()):
                ax.hist(df[data].values[:, i], color=config.COLOR)
            fig_html = mpld3.fig_to_html(fig)
            components.html(fig_html, height=600)
        except:
            st.write("It is not possible tp draw a histogram with the selected variable")



import streamlit as st
import streamlit.components.v1 as components
from streamlit_toggle import st_toggle_switch
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
        x = 'index' 
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

    data_cols = st.multiselect("Columns:", df.columns)
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

def stepsize(x):
    min_ = np.nanmin(x)
    max_ = np.nanmax(x)
    diff = (max_ - min_)
    if diff <= 100:
        step = 1
    else:
        step = int(diff / 100)
    return step

def line(df):
    '''
    draw a linechart 
    ::in param:: dataframe
    '''
    if st.checkbox("Show explanation for 'Linechart'"):
        st.markdown(explanations.LINECHART)
    # get variables
    st.session_state["x"], st.session_state["y"], st.session_state["sep"] = select_vars(df, type='line')
    if st.session_state["x"] == 'index':
        st.session_state["x"] = df.index
    else:
        st.session_state["x"] = df[st.session_state["x"]].values
    st.session_state["y"] = df[st.session_state["y"]].values
    
    if "level_param" not in st.session_state: 
        st.session_state["level_param"] = 95
    if "errorbar" not in st.session_state:
        st.session_state["errorbar"] = ('ci', st.session_state["level_param"])
    if "err_style" not in st.session_state:
        st.session_state["err_style"] = 'band'
    if st.checkbox("Errorbar options"):
        st.markdown(explanations.ERRORLINE)
        st.session_state["level_param"] = st.slider('Percentage of errorbar shown', 
                min_value=0, max_value=100, step=5, value=95, 
                help="select percentage of for errorbar")
        st.session_state["errorbar"] = st.radio(label='What type of error bar?', 
                options=(('ci', st.session_state["level_param"]), ('pi', st.session_state["level_param"]), ('se', st.session_state["level_param"]), ('sd', st.session_state["level_param"])),
                horizontal=True,
                help="(error bar method, percentage of error shown); https://seaborn.pydata.org/generated/seaborn.lineplot.html")
        st.session_state["err_style"] = st.radio(
                label="Error bar style",
                options=('band', 'bars'),
                horizontal=True,
                help="style of the errorbars")
  
    if "marker" not in st.session_state:
        st.session_state["marker"] = 'None'
    if "marker_show" not in st.session_state:
        st.session_state["marker_show"] = None
    if "xmin" not in st.session_state:
        st.session_state["xmin"] = int(np.nanmin(st.session_state["x"]))
        st.session_state["xmax"] = int(np.nanmax(st.session_state["x"]))
        st.session_state["ymin"] = int(np.nanmin(st.session_state["y"]))
        st.session_state["ymax"] = int(np.nanmax(st.session_state["y"]))
    if "orient" not in st.session_state:
        st.session_state["orient"] = False
    if st.checkbox("Other plot options"):
        value = list(config.MARKER_DICT.keys()).index(st.session_state["marker"])
        marker = st.radio(label='Show markers on the line', 
                options=config.MARKER_DICT.keys(), 
                horizontal=True, 
                index=value)
        st.session_state["marker_show"] = config.MARKER_DICT[marker]
        st.session_state["marker"] = marker
        change = st_toggle_switch(
                label="Change orientation",
                default_value=False, #st.session_state["orient"],
                label_after=True,
                inactive_color=config.COLOR_INACTIVE,
                active_color=config.COLOR,
                track_color=config.COLOR_TRACK
                )
        st.session_state["orient"] = change
        if change:
            xx = st.session_state["x"]
            st.session_state["x"] = st.session_state["y"]
            st.session_state["y"] = xx
        st.session_state["xmin"] = st.slider(label="Minimum for x-axis", 
                min_value=int(np.nanmin(st.session_state["x"])), 
                max_value=int(np.nanmax(st.session_state["x"])), 
                step=stepsize(st.session_state["x"]), 
                value=st.session_state["xmin"], 
                help="select minimum value for x axis")
        st.session_state["xmax"] = st.slider(label="Maximun for x-axis", 
                min_value=int(np.nanmin(st.session_state["x"])), 
                max_value=int(np.nanmax(st.session_state["x"])), 
                step=stepsize(st.session_state["x"]), 
                value=st.session_state["xmax"], 
                help="select maximum value for x axis")
        st.session_state["ymin"] = st.slider(label="Minimum for y-axis", 
                min_value=int(np.nanmin(st.session_state["y"])), 
                max_value=int(np.nanmax(st.session_state["y"])), 
                step=stepsize(st.session_state["y"]), 
                value=st.session_state["ymin"], 
                help="select minimum value for y axis")
        st.session_state["ymax"] = st.slider(label="Maximun for x-axis", 
                min_value=int(np.nanmin(st.session_state["y"])), 
                max_value=int(np.nanmax(st.session_state["y"])), 
                step=stepsize(st.session_state["y"]), 
                value=st.session_state["ymax"], 
                help="select maximum value for y axis")
 
    try:
        fig, ax = plt.subplots()
        sns.set_palette(config.PALETTE)
        sns.lineplot(data=df, y=st.session_state["y"], x=st.session_state["x"], 
                hue=st.session_state["sep"], ax=ax, marker=st.session_state["marker_show"], 
                errorbar=st.session_state["errorbar"]) #, err_stype=st.session_state["err_style"])
        ax.set_xlim(st.session_state["xmin"], st.session_state["xmax"])
        ax.set_ylim(st.session_state["ymin"], st.session_state["ymax"])
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

    y, x, sep = select_vars(df, type='hist')

    bins = st.slider('nr. of bins', min_value=5, max_value=100, step=5, value=20, help="select the nr. of bins for the histogram")
    stat = st.radio(
        label="Aggregate statistic to compute in each bin",
        options=('count', 'frequency', 'probability', 'density'),
        help="count: number of observations in each bin; frequency: number of observations divided by the bin width; probability: normalize such that bar heights sum to 1; percent: normalize such that bar heights sum to 100; density: normalize such that the total area of the histogram equals 1; more info: https://seaborn.pydata.org/generated/seaborn.histplot.html",
        horizontal=True)
    element = st.radio(
            label='Visual representation of the histogram statistic',
            options=('bars', 'step', 'poly'),
            horizontal=True
            )
    cum = st_toggle_switch(
            label="Plot the cumulative counts as bins increase",
            default_value=False,
            label_after=True,
            inactive_color=config.COLOR_INACTIVE, 
            active_color=config.COLOR,
            track_color=config.COLOR_TRACK,  
            )
    kde = st_toggle_switch(
            label="compute a kernel density estimate to smooth the distribution",
            default_value=False,
            label_after=True,
            inactive_color=config.COLOR_INACTIVE,
            active_color=config.COLOR,
            track_color=config.COLOR_TRACK,  
            )
    hz = st_toggle_switch(
            label="switch x and y axis",
            default_value=False,
            label_after=True,
            inactive_color=config.COLOR_INACTIVE,
            active_color=config.COLOR,
            track_color=config.COLOR_TRACK,
            )
    if hz:
        xx = y
        y = x
        x = xx
    try:
        fig, ax = plt.subplots()
        sns.set_palette(config.PALETTE)
        sns.histplot(data=df, x=x, y=y, hue=sep, bins=bins, stat=stat, cumulative=cum, element=element, kde=kde)
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
        st.pyplot(fig)
        #fig_html = mpld3.fig_to_html(fig)
        #components.html(fig_html, height=600)

    except:
        st.write("It is not possible to draw a Ridgeline plot")

def hist_multiple(df):
    '''
    plot histograms of multiple variables in df
    ::in params:: dataframe
    '''
    if st.checkbox("Show explanation for 'Histogram'"):
        st.markdown(explanations.HISTOGRAM)
    
    data = select_vars_for_multiple_plots(df, type_='no_group')
    nr_vars = df[data].values.shape[1]
    st.markdown('---')

    alpha = st.slider('transparency', min_value=0.0, max_value=1.0, step=0.1, value=0.8, help="select the transparency (alpha) value")
    hist_switch = st_toggle_switch(
       label="Show all variables in one plot",
        key="one_plot",
        default_value=False,
        label_after=False,
        inactive_color=config.COLOR_INACTIVE,  # optional
        active_color=config.COLOR,  # optional
        track_color=config.COLOR_TRACK,  # optional
    )
    if hist_switch:
        try:

            bins = st.slider('nr. of bins', min_value=5, max_value=100, step=5, value=20, help="select the nr. of bins for the histogram")
            fig, ax = plt.subplots()
            sns.set_palette(config.PALETTE)
            sns.histplot(data=df[data], alpha=alpha, bins=bins, ax=ax)
            fig_html = mpld3.fig_to_html(fig)
            components.html(fig_html, height=600)
        except:
            st.write("It is not possible tp draw a histogram with the selected variable")

    else:
        rows = int(np.ceil(nr_vars/3))
        try:
            fig = plt.figure(figsize=(15, rows*5))
            plt.subplots_adjust(hspace=0.5)
            sns.set_palette(config.PALETTE)
            bins = st.slider('nr. of bins', min_value=5, max_value=100, step=5, value=20, help="select the nr. of bins for the histogram")
            for i in range(nr_vars):
                n = rows*100 + 30 + i + 1
                ax = plt.subplot(n)#plt.subplots(rows, 3, figsize=(rows*5, 15))
                sns.histplot(data=df[data].values[:, i], color=config.COLOR, ax=ax, alpha=alpha, bins=bins)
            st.pyplot(fig)
        except:
            st.write("It is not possible to draw a histogram with the selected variable")



import streamlit as st
from streamlit_extras.stoggle import stoggle
import matplotlib.pyplot as plt
import seaborn as sns
import joypy
import config

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

def select_vars_for_multiple_plots(df):
    '''
    select variables to plot
    '''
    data_cols = []
    for col in df.columns:
        if st.checkbox(col):
            data_cols.append(col)

    x_list = ['index']
    x_list.extend(list(set(df.columns.to_list()) - set(data_cols)))
    col_x = st.selectbox(
            'Select a variable to group data',
            x_list)
    if col_x == 'index':
        by = None
    else:
        by = col_x

    return data_cols, by

def line(df):
    '''
    draw a linechart 
    ::in param:: dataframe
    '''
    if st.checkbox('Show explanation'):
        st.markdown("A **linechart** is a graphical representation, which connects a series of datapoints. It is often used for time dependend data. The x-axis is then chosen to be the time. It can particulary be used to show trends over time.\nHere you can choose a variable for the x-axis, for the y-axis and an optional variable to group the data. Grouping can be useful, when you want to see the effect of the y-variable on different classes in another variable. In the default data loaded you could choose 'Potability' as grouping variable.")
    x, y, sep = select_vars(df, type='line')

    try:
        fig, ax = plt.subplots()
        sns.set_palette(config.PALETTE)
        sns.lineplot(data=df, y=y, x=x, hue=sep, ax=ax)
        st.pyplot(fig)
    except:
        st.write("It is not possible to draw a linechart with the selected column")

def scatter(df):
    '''
    plot a scatterplot of two selected variables grouped by an optinal third variable.
    ::in param:: dataframe
    '''
    if st.checkbox('Show explanation'):
        st.markdown('A **scatterplot** visualizes data points using dots of two (different) numeric variables. The position of each value of the two variables on the x- and y-axis defines the value for each data point in the scatter plot. Scatter plots are used to observe relationships between variables.')
    
    x, y, sep = select_vars(df, type='scatter')

    try: 
        fig, ax = plt.subplots()
        sns.set_palette(config.PALETTE)
        sns.scatterplot(data=df, x=x, y=y, hue=sep, ax=ax)
        st.pyplot(fig)
    except:
        st.write("It is not possible to draw a scatterplot with the selected variables.")

def hist(df):
    '''
    plot a histogram of.
    ::in param:: dataframe
    '''
    if st.checkbox('Show explanation'):
        st.markdown('A **histogram** shows the frequency distribution of a variable. The values are grouped into bins and each bin is represented by a bar, that indicates the number of data points within that bin.')

    x, y, sep = select_vars(df, type='hist')

    bins = st.slider('nr. of bins', min_value=5, max_value=100, step=5, value=20, help="select the nr. of bins for the histogram")
    try:
        fig, ax = plt.subplots()
        sns.set_palette(config.PALETTE)
        sns.histplot(data=df, x=x, y=y, hue=sep, bins=bins)
        st.pyplot(fig)
    except:
        st.write("It is not possible tp draw a histogram with the selected variable")

def ridgeline(df):
    '''
    ridgeline plot
    '''
    if st.checkbox("Show explanation"):
        st.markdown("A **Ridgeline plot** shows the distribution  of one or more numeric variables. You can either choose a set of columns in order to see their distributions vertically ordered or you can choose a variable to see the distribution for each value in the grouped column.")
        st.markdown("For example in the default example you can plot the distributions of the different water parameters or you can group them by the variable 'Potability'")
    
    st.markdown("Choose the variables you would like to plot")
    data, by = select_vars_for_multiple_plots(df)
    try:
        # https://python-charts.com/distribution/ridgeline-plot-matplotlib/#:~:text=84%20Next-,Ridgeline%20plots%20with%20the%20joyplot%20function,variables%20of%20the%20data%20frame.
        fig, ax = joypy.joyplot(df, by=by, column=data) #joypy.joyplot(data, by=by)
        st.pyplot(fig)
    except:
        st.write("It is not possible to draw a Ridgeline plot")



import streamlit as st
from utils_ml import (select_data,
                      preprocess_data,
                      scale,
                      train_valid_test_split,
                      rf_class)

st.sidebar.markdown("# Machine Learning :penguin:")
st.markdown("# Machine Learning :penguin:")

if "dataframe" in st.session_state:
    df=st.session_state["dataframe"]

## select data
if 'y_col' not in st.session_state:
    st.session_state['y_col']=''
if 'x_col' not in st.session_state:
    st.session_state['x_col']=''

st.markdown("Select input and target data for your model. When you are done uncheck the 'Select Input and Target Variable' checkbox for a better overview.")
if st.checkbox('Select Input and Target Variable'):
    st.session_state['y'], st.session_state['X'], st.session_state['y_col'], st.session_state['x_col'] = select_data(df)
if st.session_state['y_col']=='':
    st.markdown("**No target variable selected yet**")
    st.markdown("Select the above checkbox to select a target variable")
else:
    st.markdown(f"**Selected target variable:** {st.session_state['y_col']}")
if st.session_state['x_col']=='':
    st.markdown("**No input data selected yet**")
    st.markdown("Select the above checkbox to select input variables")
else:
    st.markdown(f"**Selected input variables:** {st.session_state['x_col']}")

## preprocessing
if st.session_state['x_col']!='':
    st.markdown("**Preprocess your data before training.**")
    nans = st.selectbox('How do you want to treat missing values?', ['', 'remove'])
    if nans == 'remove':
        st.session_state['y'], st.session_state['X'] = preprocess_data(df, st.session_state['x_col'], st.session_state['y_col'], nans)
        st.markdown("Missing data was removed.")
        st.markdown(f"Target data shape: {st.session_state['y'].shape}")
        st.markdown(f"Input data shape: {st.session_state['X'].shape}")

## split data
if st.session_state['x_col']!='':
    st.markdown("**Split your Data before Training**")
    splits = st.selectbox('How many Splits do you want?', ["Training and Validation", "Training, Validation and Test"])
    if splits == "Training and Validation":
        test = False
    else:
        test = True

    if st.session_state['x_col']:
        X_train, X_valid, X_test, y_train, y_valid, y_test = train_valid_test_split(st.session_state['X'], st.session_state['y'], test)
        st.session_state['X_train'] = X_train
        st.session_state['X_valid'] = X_valid
        st.session_state['X_test'] = X_test
        st.session_state['y_train'] = y_train
        st.session_state['y_valid'] = y_valid
        st.session_state['y_test'] = y_test
        if 'X_train' in st.session_state:
            st.markdown(f"Train data length: {len(X_train)}")
            st.markdown(f"Valid data length: {len(X_valid)}")
            if test:
                st.markdown(f"Test data length: {len(X_test)}")

## scale date
if 'X_train' in st.session_state:
    st.markdown("**Do you want to scale your input data?**")
    st.markdown("The input data must be numeric (type int or float). The data is scaled using the StandardScaler from sklearn")
    if st.checkbox("Yes, scale data before modeling"):
        if 'X_train' in st.session_state:
            st.session_state['X_train'], st.session_state['X_valid'], st.session_state['X_test'] = scale(st.session_state['X_train'], st.session_state['X_valid'], st.session_state['X_test'])
            st.markdown("Your data is scaled")
        else:
            st.markdown("Your data is not split yet")

## choose model
regression_model = ['',
                    'Linear Regression', 
                    'Decission Tree', 
                    'Random Forest']

classification_model = ['',
                        'Logistic Regression',
                        'Decision Tree',
                        'Random Forest']

st.sidebar.markdown("**Regression**")
reg = st.sidebar.selectbox(
            'Select a Regression Model',
            regression_model)

st.sidebar.markdown("**Classification**")
clf = st.sidebar.selectbox(
            'Select a Classification Model',
            classification_model)

if reg=="Linear Regression":
    pass
if reg=="Decission Tree Regression":
    pass
if reg=="Random Forest Regression":
    pass

if clf=="Logistic Regresion":
    pass
if clf=="Decission Tree":
    pass
if clf=="Random Forest":
    if 'X_train' in st.session_state:
        acc_train, acc_valid, acc_test = rf_class(st.session_state['X_train'], 
                st.session_state['X_valid'],
                st.session_state['X_test'],
                st.session_state['y_train'],
                st.session_state['y_valid'],
                st.session_state['y_test'])
        st.markdown("**Modelling results:**")
        st.markdown("Accuracy:")
        st.markdown(f"Training: {acc_train:.3f}")
        st.markdown(f"Validation: {acc_valid:.3f}")
        if splits=="Training, Validation and Test":
            st.markdown(f"Test: {acc_test:.3f}")
    else:
        st.markdown("**Please select a target and input data before selecting a model.**")

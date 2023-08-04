import streamlit as st
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import config

def select_data(df):
    """
    select target and feature data
    """

    y_col = st.selectbox("Select target variable",  df.columns.to_list())

    cols = list(set(df.columns) - set(y_col))
    
    x_col = []
    st.markdown("Select the feature variables.")
    for col in cols:
        if st.checkbox(col):
            x_col.append(col)
    
    X = df[x_col].values
    y = df[y_col].values
    if x_col==[]:
        x_col=''
    return y, X, y_col, x_col

def preprocess_data(df, x_col, y_col, nans):
    # remove nans
    if nans=='remove':
        df = df.dropna()
        y = df[y_col]
        X = df[x_col]
    return y, X

def train_valid_test_split(X, y, test=False):
    if test:
        X_train_full, X_test, y_train_full, y_test = train_test_split(X, y, test_size = 0.2, random_state=42)
        X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, y_train_full, test_size=0.25, random_state=42)
        return X_train, X_valid, X_test, y_train, y_valid, y_test
    else:
        X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_valid, None, y_train, y_valid, None


def scale(X_train, X_valid, X_test=None):
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)
    if X_test is not None:
        X_test = scaler.transform(X_test)
    return X_train, X_valid, X_test

def rf_class(X_train, X_valid, X_test, y_train, y_valid, y_test):

    clf = RandomForestClassifier()

    clf.fit(X_train, y_train)
    y_pred_valid = clf.predict(X_valid)
    accuracy_valid = accuracy_score(y_pred_valid, y_valid)
    accuracy_test = None
    if X_test is not None:
        y_pred_test = clf.predict(X_test)
        accuracy_test = accuracy_score(y_pred_test, y_test)

    return accuracy_valid, accuracy_test
    

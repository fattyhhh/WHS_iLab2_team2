import os
import streamlit as st

def set_app_config():
    
    st.set_page_config(
        page_title="Company Search - Falls Related Construction companies",
        page_icon= "🔍",
        layout="centered",
)

def set_session_state(key, value):
    
    if key in st.session_state:
        if key == 'name':
            st.session_state[key] = os.environ['Company_Name']
        elif key == 'postcode':
            st.session_state[key] = os.environ['Postcode']
        elif key == 'ABN':
            st.session_state[key] = os.environ['POSTGRES_HOST']
        elif key == 'number of results':
            st.session_state[key] = os.environ['POSTGRES_DB']
        else:
            st.session_state[key] = value

def set_session_states(keys, value=None):
    
    for key in keys:
        set_session_state(key, value)

def display_session_state():
    
    st.write(st.session_state)
    
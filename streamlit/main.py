import streamlit as st
from config import set_app_config, set_session_states, display_session_state
import psycopg2
import pandas as pd
from search import results


set_session_states(['name', 'postcode', 'ABN', 'number of results', 'activity'])

set_app_config()
st.title('Company Search - Falls Related Construction Companies')

with st.expander("Streamlit Session State", expanded=False):
    display_session_state()

st.header("Search Information Details")

st.text_input("Company Name", key='name')

st.text_input("Postcode", key='postcode') 

st.text_input("ABN", key='ABN')

st.text_input("Number of results", key='number of results')

st.text_input("Business Activity", key = 'activity')

st.button("Search")

if st.button("Search"):
    st.write("Searching...")
    st.dataframe(results(st.session_state.name, st.session_state.postcode, st.session_state.ABN, st.session_state['number of results'], st.session_state.activity))


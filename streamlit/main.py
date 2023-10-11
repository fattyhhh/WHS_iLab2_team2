import streamlit as st
from config import set_app_config, set_session_state, set_session_states, display_session_state

set_session_states(['name', 'postcode', 'ABN', 'number of results'])

set_app_config()
st.title('Company Search - Falls Related Construction Companies')

st.header("Search Information Details")

st.text_input("Company Name", key='name')

st.text_input("Postcode", key='postcode') 

st.text_input("ABN", key='ABN')

st.text_input("Number of results", key='number of results')

st.button("Search")
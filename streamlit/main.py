import streamlit as st
from search import Search
import pandas as pd



st.set_page_config(
        page_title="Company Search - Falls Related Construction companies",
        page_icon= "🔍",
        layout="centered",
)
st.title('Company Search - Falls Related Construction Companies')


df_options= pd.read_excel('Bussiness_activities.xlsx',header=0)
options = df_options["Activities"].to_list()
# options=["apple", "banana", "cherry", "date"]
st.header("Search Information Details")


activity = st.multiselect("Business Activity",options)

name = st.text_input("Company Name")

postcode = st.text_input("Postcode") 

abn = st.text_input("ABN")

num_results = st.text_input("Number of Results")



if st.button("Search"):
    # Assign input values to session state
    st.session_state.activity = activity
    st.session_state.name = name
    st.session_state.postcode = postcode
    st.session_state.abn = abn
    st.session_state.num_results = num_results
    
    
    # Perform the search using the session state values
    search = Search(name, postcode, abn, num_results, activity)
    
    # run method to get result
    search.get_result()

    # display result
    search_result = search.df_result

    if search_result is not None:
        st.table(search_result.assign(hack='').set_index('hack'))
    else:
        st.write("No results found.")
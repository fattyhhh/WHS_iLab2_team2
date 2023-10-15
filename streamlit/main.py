import streamlit as st
from search import Search




st.set_page_config(
        page_title="Company Search - Falls Related Construction companies",
        page_icon= "🔍",
        layout="centered",
)
st.title('Company Search - Falls Related Construction Companies')



st.header("Search Information Details")

name = st.text_input("Company Name")

postcode = st.text_input("Postcode") 

abn = st.text_input("ABN")

num_results = st.text_input("Number of Results")

activity = st.text_input("Business Activity")


if st.button("Search"):
    # Assign input values to session state
    st.session_state.name = name
    st.session_state.postcode = postcode
    st.session_state.abn = abn
    st.session_state.num_results = num_results
    st.session_state.activity = activity
    
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
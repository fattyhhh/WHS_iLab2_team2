import streamlit as st
from search import Search
import sys
# sys.path.insert(1, '../a2')
from scrap_function import getabn,get_links_with_same_domain,words_abn
import pandas as pd



st.set_page_config(
        page_title="Company Search - Falls Related Construction companies",
        page_icon= "🔍",
        layout="centered",
)
st.title('Company Search - Falls Related Construction Companies')


df_options= pd.read_excel('Bussiness_activities.xlsx',header=0)
options = df_options["Activities"].to_list()
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
    
    st.write(activity)
    # Perform the search using the session state values
    search = Search(name, postcode, abn, num_results, activity)
    
    # run method to get result
    search.get_result()
    # display result
    search_result = search.df_result
    if search_result.empty == False:
        st.write("Results found: " + str(len(search_result)))
        st.table(search_result.assign(hack='').set_index('hack'))
        df=search_result.copy()
        csv=df.to_csv(index=False).encode('utf-8')
        download = st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='ABN_users_searchs.csv',
        mime='text/csv'
        )
        st.session_state.df = df
    else:
        st.write("No results found.")
def postcode(location):
    return location[-4:]

if 'df' in st.session_state:
    if st.button("Get up-to-date ABN numbers"):
        #display columns
        st.session_state.df['postcode'] = st.session_state.df['location'].apply(postcode)
        st.session_state.df['name_postcode'] = st.session_state.df['name']+st.session_state.df['postcode']
        st.session_state.df['ABN_lookup_new'] = st.session_state.df['name_postcode'].apply(getabn)
        st.session_state.df['Contents']=st.session_state.df['website'].apply(get_links_with_same_domain)
        st.session_state.df['abn_website'] = st.session_state.df['Contents'].apply(words_abn)
        st.session_state.df['ABN_up_to_date'] = st.session_state.df['abn_website'].fillna(st.session_state.df['ABN_lookup_new']).fillna(st.session_state.df['abn'])
        #drop not used columns
        st.session_state.df=st.session_state.df.drop(columns=['name_postcode','Contents','abn','ABN_lookup_new','abn_website'])

        st.table(st.session_state.df.assign(hack='').set_index('hack'))
        csv=st.session_state.df.to_csv(index=False).encode('utf-8')
        download = st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='ABN_users_searchs.csv',
        mime='text/csv'
        )

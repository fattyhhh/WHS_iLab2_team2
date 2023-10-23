import pandas as pd
import streamlit as st
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
def Abn_search(keywords,df):
    results = []
    for index, row in df.iterrows():
        content = row['contents']

        # Check if all keywords are present in the 'Contents' column
        keyword_token = []

        for keyword in keywords:
            keyword = keyword.lower()
            keyword_tokenized = word_tokenize(keyword)
            
            keyword_token.append(keyword_tokenized)
        
        # flatten the list
        keyword_token = [item for sublist in keyword_token for item in sublist]
        
        # drop the duplicates to optimaise the search
        keyword_token = pd.Series(keyword_token).drop_duplicates(keep= 'first').tolist()

        # drop construction from the keywords to get more precise results
        keyword_token = [keyword for keyword in keyword_token if keyword != 'construction']
        
        # loop on tokenized keywords
        for keyword in keyword_token:
            if keyword in content.lower():
        
                
                abn = row['abn_website'] if not pd.isnull(row['abn_website']) else (
                    row['abn_look_up'] if not pd.isnull(row['abn_look_up']) else row['abn']
                    )

                results.append({
                        'abn': abn,
                        'name': row['name'],
                        'location': row['location'],
                        'website': row['website'],
                        'postcode': row['postcode']
                    })

    
    # Convert the list of dictionaries to a DataFrame
    results_df = pd.DataFrame(results).drop_duplicates()
    
    return results_df
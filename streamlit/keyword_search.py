import pandas as pd
import streamlit as st

def Abn_search(keywords,df):
    results = []
    for index, row in df.iterrows():
        content = row['contents']

        # Check if all keywords are present in the 'Contents' column
        for keyword in keywords:
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
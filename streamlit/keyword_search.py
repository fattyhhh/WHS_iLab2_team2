import pandas as pd


def Abn_search(keywords, df1):
    results = []
    for keyword in keywords:
        # Search 'web contents' column for keywords and extract corresponding data
        filtered_data = df1[df1['web_content'].str.contains(keyword, case=False, na=False)]
        for index, row in filtered_data.iterrows():
            results.append({
                'abn': row['abn_look_up'],
                'name' : row['name'],
                'location': row['location'],
                'website': row['website']
            })
    # Convert the list of dictionaries to a DataFrame
    results_df = pd.DataFrame(results).drop_duplicates()
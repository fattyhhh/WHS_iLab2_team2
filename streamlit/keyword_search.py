import pandas as pd


def Abn_search(keywords,df):
    results = []
    for index, row in df.iterrows():
        content = row['Contents']
        # Check if all keywords are present in the 'Contents' column
        if all(keyword.lower() in content.lower() for keyword in keywords):
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

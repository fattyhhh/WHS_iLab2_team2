import re
import pandas as pd
import numpy as np

#Create cleaned dataset
df_cleaned=pd.read_excel('final_data.xlsx', header=0)
df_cleaned=df_cleaned[df_cleaned['Contents'].notnull()]

# Create postcode column
def postcode(location):
    return location[-4:]
df_cleaned['postcode'] = df_cleaned['location'].apply(postcode)
#Extract ABN from website contents
def extract_abn(text):
    match = re.search(r'(\d{11})', text)
    if match:
        return match.group(1)
    else:
        return None
    
def words_abn(text):
    #get 15 character before ABN and 14 chars after ABN in web contents
    match = re.search(r's*(.{15})ABN\s*(.{14})', text, re.IGNORECASE)
    match2 = re.search(r'ABN\s*NSW\s*(.{15})', text, re.IGNORECASE)
    if match2:
        return extract_abn(match2.group(1).replace(" ", ""))
    elif match:
        abn1=extract_abn(match.group(1).replace(" ", ""))
        abn2=extract_abn(match.group(2).replace(" ", ""))
        if abn1 ==None and abn2 == None:
            return None
        elif abn1 ==None and abn2 !=None:
            return abn2
        elif abn1 !=None and abn2 ==None:
            return abn1
        else:
            return abn1,abn2
    else:
        return None
# Apply the function to the 'contents' column
df_cleaned['abn_website'] = df_cleaned['Contents'].apply(words_abn)

print(df_cleaned['abn_website'])
df_cleaned.to_excel("construction_data.xlsx", index=False)



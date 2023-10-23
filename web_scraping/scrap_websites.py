import requests
import json
import re
import pandas as pd
import time
import numpy as np
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse, urljoin

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#Create a function to request a get request with timeout is 30 seconds
def request_api(url,verify,headers):
    try:
        with requests.Session() as rs_api:
                response = rs_api.get(url, verify=verify, headers=headers,timeout=30)
                return response
    except Exception:
        return False
# Create a funtion to scrapt all text in a specific website
def web_scrap(url,headers):
    try:
        response=request_api(url=url,verify=False,headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            text = text.replace('\n', ' ').replace('\t', ' ').replace('\xa0', ' ')
            text=re.sub(' +', ' ', text)
            text=re.sub(r'[^A-Za-z0-9 ]+', '', text)
            return text
        else:
            error_msg=f"Failed to retrieve content from {url}. Status code: {response.status_code}"
            return error_msg
    except Exception:
        return ' '
#Get links inside each website with the same domain and scrapt contents for each of them.    
def get_links_with_same_domain(url,get_called=False,headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}):
    if url==None or url == 'nan':
        return None
    else:
        url=str(url)

    if 'facebook' in url:
        return None
    elif 'pinkpages.com.au' in url:
        return None
    elif 'yellowpages.com.au' in url:
        return None

    links_dict=[]
    contents=''
    response=request_api(url=url,verify=False,headers=headers)
    if response==False:
        return None
    elif response.status_code == 200:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception:
            return None
        domain = urlparse(url).netloc 
        if domain.startswith('www.'):
            domain = domain[4:]
        # Find all <a> tags in the HTML content
        links = soup.find_all('a', href=True)
        if len(links) ==0:
            if not get_called:
                return get_links_with_same_domain(url,get_called=True,headers={})
        # Filter links that belong to the same domain and then scrap all text from all sublinks then combine them
        for link in links:
            href = link['href']
            
            absolute_url = urljoin(url, href) 
            absolute_url_domain=urlparse(absolute_url).netloc
            if absolute_url_domain.startswith('www.'):
                absolute_url_domain = absolute_url_domain[4:]
            if absolute_url_domain == domain and absolute_url not in links_dict and absolute_url.endswith(('.jpg','.png','.jpeg'))==False:
                print(absolute_url)
                links_dict.append(absolute_url)
                contents=contents+' '+web_scrap(url=absolute_url,headers=headers)
                
        return contents
    else:
        return None
#Read scrapted database
df = pd.read_excel('yellowpages.xlsx', header=0)
chunk_size = 10
num_splits = int(np.ceil(len(df) / chunk_size))

# Split the DataFrame into smaller DataFrames
small_dfs = np.array_split(df, num_splits)

# Split dataframe to mutiple smaller dataframe then apply scrapping data function
for i, small_df in enumerate(small_dfs, 1):
    small_df['website'].fillna('nan', inplace=True)
    small_df['Contents']=small_df['website'].apply(get_links_with_same_domain)
    file_name = f"small_df_{i}.xlsx"
    small_df.to_excel(file_name, index=False)
    print(f"Small DataFrame {i} created")
    
#Combine all the database to one database        
combined_df = pd.concat(pd.read_excel(f"small_df_{i}.xlsx") for i in range(1, num_splits + 1))
combined_df.to_excel("uncleaned_data.xlsx", index=False)

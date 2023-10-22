import requests
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from a2.web_scrap.ABNscrap import getabn
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.yellowpages.com.au',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}
# Scraping all information from yellow pages
all_data = []
with requests.Session() as s:
    for i in range(1, 30):
        url_to = 'https://www.yellowpages.com.au/find/builders-building-contractors/nsw/page-' + str(i)
        print(url_to)
        r = s.get(url_to, verify=False, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        scripts = soup.find_all(lambda tag: tag.name == 'script' and not tag.attrs)
        
        initial_state = {}
        for script in scripts:
            if 'INITIAL_STATE' in script.contents[0]:            
                ss = script.contents[0].strip()            
                txt = re.search(r'= {(.*)};', ss).group(1)
                initial_state = json.loads('{' + txt + '}')        
                data = initial_state['model']['inAreaResultViews']
                all_data.append(data)
                

#Due to the limit memmory space, so the extracted data from yellowpages are divided into 2
all_data_1=all_data[:15]   
all_data_2=all_data[15:]  
data_csv_1 = []
data_csv_2 = []
# Scraping ABN lookup tool by using information from yellowpages
with requests.Session() as rs1:
    for data in all_data_1:# Get ABNs from yellowpages
        for row in data:
            url = row['detailsLink']  
            # Send a GET request to the webpage
            response = rs1.get(url, verify=False, headers=headers)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content 
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find all elements with the tag <dd> and class "abn"
                abn_elements = soup.find_all('dd', class_='abn')
                # Check if any elements were found
                if abn_elements:
                    # Extract and print the contents of each element
                    for abn_element in abn_elements:
                        abn_info = abn_element.get_text()
                else:
                    abn_info=None
            else:
                print(f"Failed to fetch the webpage. Status code: {response.status_code}")            
            #Get ABN from ABN look up tool 
            get_abn= getabn(row['name'].replace(" ", "+").replace("&","%26"),row['categoryText'].split('-')[1][-4:])

            if len(get_abn)==0:
                data_csv_1.append({
                    'name': row['name'],
                    'website': row['website'],
                    'location': row['categoryText'].split('-')[1],
                    'detail_url': row['detailsLink'],
                    'abn': abn_info,
                    'abn_look_up': None
                })

            else:
                data_csv_1.append({
                    'name': row['name'],
                    'website': row['website'],
                    'location': row['categoryText'].split('-')[1],
                    'detail_url': row['detailsLink'],
                    'abn': abn_info,
                    'abn_look_up': get_abn
                })
        
with requests.Session() as rs2:
    for data in all_data_2:
        for row in data:
            url = row['detailsLink']  
            # Send an HTTP GET request to the webpage
            response = rs2.get(url, verify=False, headers=headers)
            # Check if the request was successful 
            if response.status_code == 200:
                # Parse the HTML content 
                soup = BeautifulSoup(response.text, 'html.parser')
                # Find all elements with the tag <dd> and class "abn"
                abn_elements = soup.find_all('dd', class_='abn')
                # Check if any elements were found
                if abn_elements:
                    # Extract and print the contents of each element
                    for abn_element in abn_elements:
                        abn_info = abn_element.get_text()
                else:
                    abn_info=None
            else:
                print(f"Failed to fetch the webpage. Status code: {response.status_code}")
            #Get ABN from ABN look up tool             
            get_abn= getabn(row['name'].replace(" ", "+").replace("&","%26"),row['categoryText'].split('-')[1][-4:])

            if len(get_abn)==0:
                data_csv_2.append({
                    'name': row['name'],
                    'website': row['website'],
                    'location': row['categoryText'].split('-')[1],
                    'detail_url': row['detailsLink'],
                    'abn': abn_info,
                    'abn_look_up': None
                })

            else:
                data_csv_2.append({
                    'name': row['name'],
                    'website': row['website'],
                    'location': row['categoryText'].split('-')[1],
                    'detail_url': row['detailsLink'],
                    'abn': abn_info,
                    'abn_look_up': get_abn
                })

#Merge two dataset and export to an xlsx file
df1 = pd.DataFrame(data_csv_1)
df2 = pd.DataFrame(data_csv_2)
df = pd.concat([df1, df2])

df.to_excel('yellowpages5.xlsx', index=False)
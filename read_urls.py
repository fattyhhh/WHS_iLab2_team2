import requests
import json
import re
import pandas as pd
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# set headers
headers = {
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
}
all_data = []

# import website and company name from excel file
urls = pd.read_excel('yellowpages2.xlsx')
urls = urls[['name','website']]

# scrape website text and store in dataframe
# just demo for now
with requests.Session() as s:
    for i in range(2,4):
        try:
            r = s.get(urls['website'][i], verify=False, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.get_text()
            text = text.replace('\n', '').replace('\t', '')
            links = soup.find_all('a', href=True)
            links = [link['href'] for link in links]
            links = [link for link in links if (link.startswith(urls['website'][i]) and link.endswith('/'))]
            #links2 = [link for link in links if link.startswith('/')]
            #links3 = []
            #for x in len(links2):
            #    links3[x] = urls['website'][i] + links2[x]
            #print(links3)
            #links = links1 + links3
            urls['text'][i] = text
            urls['son_links'][i] = links
        except Exception as e:
            urls['text'] = 'error'
            pass    
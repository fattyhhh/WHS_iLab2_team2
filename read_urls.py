mport pandas as pd
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from urllib.parse import urljoin
import xlsxwriter
from timeout_decorator import timeout 

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
urls = pd.read_excel('yellowpages5.xlsx')
# select the rows to be scraped
urls = urls.iloc[953:958,:]
urls = urls[['name','website']]
urls['text'] = ''
urls['sublinks'] = ''
urls['sublinkstext'] = ''
# scrape website text and store in dataframe
# something wrong with index 958
with requests.Session() as s:
    # manual change the range
    for i in range(953, 958):
        try:
            print(i)
            temp = urls['website'][i].replace('https://www.','')
            r = s.get(urls['website'][i], verify=False, headers=headers)
            soup = BeautifulSoup(r.text, 'html.parser')
            text = soup.get_text()
            text = text.replace('\n', '').replace('\t', '')
            sublinks=[]
            for link in soup.find_all('a', href=True):
                absolute_link = urljoin(urls['website'][i], link['href'])
                if absolute_link not in sublinks:
                    if temp in absolute_link:
                        sublinks.append(absolute_link)
                
            urls['text'][i] = text
            urls['sublinks'][i] = sublinks
            for x in urls['sublinks'][i]:
                try:
                    t = s.get(x, verify=False, headers=headers)
                    soup1 = BeautifulSoup(t.text, 'html.parser')
                    text1 = soup1.get_text()
                    text1 = text1.replace('\n', '').replace('\t', '')
                    urls['sublinkstext'][i] = urls['sublinkstext'][i] + text1
                except:
                    print('error in sublinks')
                    print(i)
                    pass 
        except:
            print('error')
            print(i)
            pass

# need manually amend the suffix 
urls.to_excel('all_text_6_5.xlsx', engine='xlsxwriter')
           
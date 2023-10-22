import marshal
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
        contents=contents+' '+web_scrap(url,headers=headers)
        for link in links:
            href = link['href']
            
            absolute_url = urljoin(url, href) 
            absolute_url_domain=urlparse(absolute_url).netloc
            if absolute_url_domain.startswith('www.'):
                absolute_url_domain = absolute_url_domain[4:]
            if absolute_url_domain == domain and absolute_url not in links_dict and absolute_url.endswith(('.jpg','.png','.jpeg'))==False:
                if 'about' in absolute_url or 'contact' in absolute_url:
                    links_dict.append(absolute_url)
                    contents=contents+' '+web_scrap(url=absolute_url,headers=headers)
                
        return contents
    else:
        return None

import urllib.request as req
import xml.etree.ElementTree as ET


def getabn(busname_postcode):
	ABN_list=[]
	name=busname_postcode[:-4].replace(" ", "+").replace("&","%26")
	postcode=busname_postcode[-4:] 
	legalName = ''		
	tradingName = ''	
	NSW = ''			
	SA = 'N'				
	ACT = 'N'			
	VIC = 'N'			
	WA = 'N'				
	NT = 'N'				
	QLD = 'N'			
	TAS = 'N'			
	authenticationGuid = '7a2df7f7-7bf3-4561-998e-1c9882b5f854'		#Your GUID should go here

	#Constructs the URL by inserting the search parameters specified above
	#GETs the url (using urllib.request.urlopen)
	conn = req.urlopen('https://abr.business.gov.au/abrxmlsearchRPC/AbrXmlSearch.asmx/' + 
						'ABRSearchByNameSimpleProtocol?name=' + name + 
						'&postcode=' + postcode + '&legalName=' + legalName + 
						'&tradingName=' + tradingName + '&NSW=' + NSW + 
						'&SA=' + SA + '&ACT=' + ACT + '&VIC=' +  VIC + 
						'&WA=' + WA + '&NT=' + NT + '&QLD=' + QLD + 
						'&TAS=' + TAS + '&authenticationGuid=' + authenticationGuid)
	#Put returned xml into variable 'returnedXML' 
	#Output xml string to file 'output.xml' and print to console
	returnedXML = conn.read()

	root = ET.fromstring(returnedXML)
	namespace = {'ns': 'http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes'}

	# Find the <response> element within the namespace
	ABN_records = root.findall('.//ns:response/ns:searchResultsList/ns:searchResultsRecord', namespaces=namespace)
	for ABN_record in ABN_records:
		ABN = ABN_record.find('.//ns:ABN/ns:identifierValue', namespaces=namespace)
		status = ABN_record.find('.//ns:ABN/ns:identifierStatus', namespaces=namespace)
		match_score_bus = ABN_record.find('.//ns:businessName/ns:score', namespaces=namespace)
		match_score_main = ABN_record.find('.//ns:mainName/ns:score', namespaces=namespace)
		post_code= ABN_record.find('.//ns:mainBusinessPhysicalAddress/ns:postcode', namespaces=namespace)
		if match_score_main!=None and status.text=="Active" and  match_score_main.text=='100' and post_code.text == postcode :
			return ABN.text
		elif match_score_bus!=None and status.text=="Active" and  match_score_bus.text=='100' and post_code.text == postcode:
			return ABN.text
		elif match_score_bus!=None and status.text=="Active" and  match_score_bus.text=='100':
			ABN_list.append(ABN.text)
		elif match_score_main!=None and status.text=="Active" and  match_score_main.text=='100':
			ABN_list.append(ABN.text)
		else:
			pass
	return ABN_list if len(ABN_list) > 0 else None

import re
import pandas as pd
import numpy as np

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





import urllib.request as req
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
#Search parameters for ABRSearchByNameSimpleProtocol service
#Note, this service requires all parameters to be specified, even if you specify no query parameter
#The parameters specified below will search for an entity with  the name 'coles' with postcode '2250'
#In this case, unspecified search parameters all default to 'Y' 
#(i.e. will search for the legal & trading name 'coles' in all States and Territories

# def get_abn_score(busname):
# 	name = busname
# 	postcode=''
# 	legalName = ''		
# 	tradingName = ''	
# 	NSW = ''			
# 	SA = 'N'				
# 	ACT = 'N'			
# 	VIC = 'N'			
# 	WA = 'N'				
# 	NT = 'N'				
# 	QLD = 'N'			
# 	TAS = 'N'			
# 	authenticationGuid = '7a2df7f7-7bf3-4561-998e-1c9882b5f854'		#Your GUID should go here

# 	#Constructs the URL by inserting the search parameters specified above
# 	#GETs the url (using urllib.request.urlopen)
# 	conn = req.urlopen('https://abr.business.gov.au/abrxmlsearchRPC/AbrXmlSearch.asmx/' + 
# 						'ABRSearchByNameSimpleProtocol?name=' + name + 
# 						'&postcode=' + postcode + '&legalName=' + legalName + 
# 						'&tradingName=' + tradingName + '&NSW=' + NSW + 
# 						'&SA=' + SA + '&ACT=' + ACT + '&VIC=' +  VIC + 
# 						'&WA=' + WA + '&NT=' + NT + '&QLD=' + QLD + 
# 						'&TAS=' + TAS + '&authenticationGuid=' + authenticationGuid)
# # https://abr.business.gov.au/abrxmlsearchRPC/AbrXmlSearch.asmx/ABRSearchByNameSimpleProtocol?name=P+%26+L+Knight+Builders+Pty.+Ltd.&postcode=&legalName=&tradingName=&NSW=&SA=N&ACT=N&VIC=N&WA=N&NT=N&QLD=N&TAS=N&authenticationGuid=7a2df7f7-7bf3-4561-998e-1c9882b5f854	#XML is returned by the webservice
# 	#Put returned xml into variable 'returnedXML' 
# 	#Output xml string to file 'output.xml' and print to console
# 	returnedXML = conn.read()

# 	root = ET.fromstring(returnedXML)
# 	namespace = {'ns': 'http://abr.business.gov.au/ABRXMLSearchRPC/literalTypes'}

# 	# Find the <response> element within the namespace
# 	ABN_records = root.findall('.//ns:response/ns:searchResultsList/ns:searchResultsRecord', namespaces=namespace)
# 	ABN_score=[]
# 	for ABN_record in ABN_records:
# 		ABN = ABN_record.find('.//ns:ABN/ns:identifierValue', namespaces=namespace)
# 		status = ABN_record.find('.//ns:ABN/ns:identifierStatus', namespaces=namespace)
# 		match_score_bus = ABN_record.find('.//ns:businessName/ns:score', namespaces=namespace)
# 		match_score_main = ABN_record.find('.//ns:mainName/ns:score', namespaces=namespace)
# 		if match_score_bus!=None and status.text=="Active" and  match_score_bus.text=='100':
# 			ABN_score.append(ABN.text)
# 		elif match_score_main!=None and status.text=="Active" and  match_score_main.text=='100':
# 			ABN_score.append(ABN.text)
# 		else:
# 			pass
# 	return ABN_score


def getabn(busname,buspostcode):
	ABN_list=[]
	if buspostcode.isdigit()==False:
		buspostcode=''
	postcode=''
	name = busname
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
# https://abr.business.gov.au/abrxmlsearchRPC/AbrXmlSearch.asmx/ABRSearchByNameSimpleProtocol?name=P+%26+L+Knight+Builders+Pty.+Ltd.&postcode=&legalName=&tradingName=&NSW=&SA=N&ACT=N&VIC=N&WA=N&NT=N&QLD=N&TAS=N&authenticationGuid=7a2df7f7-7bf3-4561-998e-1c9882b5f854	#XML is returned by the webservice
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
		if match_score_main!=None and status.text=="Active" and  match_score_main.text=='100' and post_code.text == buspostcode :
			return ABN.text
		elif match_score_bus!=None and status.text=="Active" and  match_score_bus.text=='100' and post_code.text == buspostcode:
			return ABN.text
		elif match_score_bus!=None and status.text=="Active" and  match_score_bus.text=='100':
			ABN_list.append(ABN.text)
		elif match_score_main!=None and status.text=="Active" and  match_score_main.text=='100':
			ABN_list.append(ABN.text)
		else:
			pass
	return ABN_list





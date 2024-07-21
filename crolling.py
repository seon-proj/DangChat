from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader

from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from bs4 import BeautifulSoup
import requests
import re
import tiktoken
 

def concat(title : str, value : str):
    title = re.sub(r':', '', title.strip())
    value = re.sub(r':', '', value.strip())
    return title + " : " + value

def crolling(soup, result_list: []):
    result = []
    title = soup.find('h3', class_='tit_board_view').text
    # print(title)
    result.append(title)
    details_group = soup.find_all('div', class_='group')
    
    details = details_group[0].find_all('dd')
    details_title = details_group[0].find_all('dt')
    volunteer_duration : str = concat(details_title[0].text, details[0].text)
    volunteer_time : str = concat(details_title[1].text, details[1].text)
    result.append(volunteer_duration)
    result.append(volunteer_time)
    details = details_group[1].find_all('dd')
    details_title = details_group[1].find_all('dt')
    recruit_number : str = concat(details_title[0].text, details[0].text) 
    register_number : str = concat(details_title[1].text, details[1].text)
    result.append(recruit_number)
    result.append(register_number)
    details = details_group[2].find_all('dd')
    details_title = details_group[2].find_all('dt')
    voluntary_category : str = concat(details_title[0].text, details[0].text)
    volunteer_category : str = concat(details_title[1].text, details[1].text)
    result.append(voluntary_category)
    result.append(volunteer_category)

    details = details_group[3].find_all('dd')
    details_title = details_group[3].find_all('dt')
    agency : str = concat(details_title[0].text, details[0].text) 
    register_agency : str = concat(details_title[1].text, details[1].text)
    result.append(agency)
    result.append(register_agency)

    details = details_group[4].find_all('dd')
    details_title = details_group[4].find_all('dt')
    volunteer_location : str = concat(details_title[0].text,details[0].text)
    volunteer_target : str = concat(details_title[1].text,details[1].text)
    result.append(volunteer_location)
    result.append(volunteer_target)
    
    details_group = soup.find_all('div', class_='group group_dl1')
    details = details_group[0].find('dd')
    details_title = details_group[0].find('dt')
    active_category : str = concat(details_title.text, details.text)
    result.append(active_category)

    details = details_group[1].find('dd') 
    details_title = details_group[1].find('dt')
    file : str = concat(details_title.text, details.text)
    result.append(file)
    desc = soup.find('div', class_='bb_txt').find('pre').text  
    result.append(desc)

    manager = concat(soup.find('dl', class_='name').find('dt').text, soup.find('dl', class_='name').find('dd').text)
    mgr_phone = concat(soup.find('dl', class_='tel').find('dt').text, soup.find('dl', class_='tel').find('dd').text)
    mgr_fax = concat(soup.find('dl', class_='fax').find('dt').text, soup.find('dl', class_='fax').find('dd').text)
    mgr_place = concat(soup.find('dl', class_='addr').find('dt').text, soup.find('dl', class_='addr').find('dd').text)
    result.append(manager)
    result.append(mgr_phone)
    result.append(mgr_place)
    result.append(mgr_fax)

    result_str = ' '.join(result)
    result_list.append(result_str)
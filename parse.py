from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.schema import Document
import crolling as cr
from langchain_community.chat_models import ChatOpenAI
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

from bs4 import BeautifulSoup
import requests
import tiktoken

from numpy import dot
from numpy.linalg import norm
import numpy as np

import streamlit as st

START_PAGE = 0
PAGING = 10
TODAY = '2024.07.19'

load_dotenv()

headers= {
    "Content-Type: text/html;charset=UTF-8"
}
st.title("Welcome! This is 댕CHAT")

chat_model = ChatOpenAI()
content = st.text_input('유기견 봉사와 관련된 정보를 찾아보세요')
# def error_handling(url):
#     req = Request(url)
#     try:
#         response=urlopen(req, headers = headers)
#     except HTTPError as e:
#         print(e)
#     except URLError as e:
#         print("The server could not be found")
#     except AttributeError as e:
#         return None
#     except UnicodeEncodeError as e:
#         return response.read().decode('utf-8')

def cos_sim(A,B):
    return dot(A,B)/(norm(A) * norm(B))



BASE_1365_URL = '/vols/search.do?collection=personalserve&startCount=0&sort=RANK&cateSearch=all&range=A&startDate=1970.01.01&endDate='+TODAY+'&searchField=ALL&reQuery=2&realQuery=%EC%9C%A0%EA%B8%B0%EA%B2%AC&query=%EC%9C%A0%EA%B8%B0%EA%B2%AC'

URL_PREFIX = "https://www.1365.go.kr/"



def get_soup(url):
    response = requests.get(url).text
    # response.raise_for_status()  # Raise an exception for HTTP errors
    return BeautifulSoup(response, 'html.parser')

def find_next_page(soup):
    next_button = soup.find('a', class_='tit')
    if next_button and 'href' in next_button.attrs:
        return next_button['href']
    return None

result_list=[]

def main(current_url):
    print("-----------------url------------------")
    soup = get_soup(current_url)
    cr.crolling(soup, result_list)
    

base_url = URL_PREFIX + BASE_1365_URL  # Starting page URL
has_next = True

if has_next:
    # find_next_page(base_url) 
    urls = get_soup(base_url).find_all('a' ,class_='tit')
    URL_LIST_PREFIX = "https://www.1365.go.kr"
    print(len(urls)) 
    for url in urls:
        # error_handling(URL_LIST_PREFIX+url.get('href'))
        main(URL_LIST_PREFIX+url.get('href'))


model_name = "jhgan/ko-sbert-nli"
model_kwargs = { 'device' : 'cpu' }
encode_kwargs = { 'normalize_embeddings' : True}


embeddings_model = OpenAIEmbeddings()

print(result_list)
embeddings = embeddings_model.embed_documents(
    result_list
)

len(embeddings), len(embeddings[0])

q = "유기견 봉사활동을 할 수 있는 모든 지역 중 성남시 근처를 알려주세요"
# BGE_query_q = .embed_query(q)
#----------------------------------------------
BGE_query_q=embeddings_model.embed_query(q)
tokenizer = tiktoken.get_encoding("cl100k_base")

def tiktoken_len(text):
    tokens = tokenizer.encode(text)
    return len(tokens)

documents = [Document(page_content=text) for text in result_list]

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0, length_function=tiktoken_len)

# docs = text_splitter.split_documents(result_list)

db = Chroma.from_documents(documents, embeddings_model)

query = '서울시 동작구 상도동에서 가장 가까운 유기견 봉사활동 한개만 알려줘'
docs = db.similarity_search(query) 

# print(docs)
# print("-----------------------")
# print(docs[0].page_content)


if st.button(" -> "):
    with st.spinner("댕댕이가 삶을 구한다..."):
        result=db.similarity_search(content) 
        st.write(result)


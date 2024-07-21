from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv
# with open('./123.pdf', encoding='cp1252') as f:
#     state_of_union = f.read()
loader = WebBaseLoader("https://www.1365.go.kr/vols/search.do?collection=personalserve&startCount=0&sort=RANK&cateSearch=all&range=A&startDate=1970.01.01&endDate=2024.06.16&searchField=ALL&reQuery=2&realQuery=%EC%9C%A0%EA%B8%B0%EA%B2%AC&query=%EC%9C%A0%EA%B8%B0%EA%B2%AC")
state_of_union = loader.load()

load_dotenv()
print(state_of_union)
text_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size= 1000,
    chunk_overlap = 100, # 전 청크의 마지막문단을 맥락을 확인하도록!
    length_function = len, # 글자수 기준
)

# 청크
# texts = text_splitter.split_text(state_of_union)
# print(texts[0])
# print("-"*100)
# print(texts[10])

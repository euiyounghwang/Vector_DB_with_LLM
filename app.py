
# Load documents from web
# from langchain.document_loaders import WebBaseLoader

# web_loader = WebBaseLoader([
#     "https://python.langchain.com/docs/get_started/introduction",   # LangChain Introduction
#     "https://python.langchain.com/docs/modules/data_connection/" # LangChain Retrieval
#     ]
# )

''' https://colab.research.google.com/github/i-am-shuan/learn-langchain/blob/main/langchain_RAG_example.ipynb#scrollTo=S79kQe04X2-j '''
from langchain.document_loaders import PyPDFLoader

# loader = PyPDFLoader("https://snuac.snu.ac.kr/2015_snuac/wp-content/uploads/2015/07/asiabrief_3-26.pdf")
loader = PyPDFLoader("./asiabrief_3-26.pdf")
pages = loader.load_and_split()
print(pages)

print('\n\n')

# PDF 내용을 작은 chunk 단위로 나누기
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(pages)
print(pages)
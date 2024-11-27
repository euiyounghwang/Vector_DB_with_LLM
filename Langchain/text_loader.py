
from langchain_community.document_loaders import TextLoader # type: ignore
from langchain_community.document_loaders import DirectoryLoader # type: ignore
from langchain.document_loaders import PyPDFLoader # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
''' split characters  ["\n\n", "\n", " ", ""]'''
''' length_function , chunk_size , chunk_overlap, add_start_index (Determines whether to include the start position of the chunk within the original document in the metadata) '''


import warnings
warnings.filterwarnings("ignore")
import os
os.environ['CURL_CA_BUNDLE'] = ''

# current_path = os.path.dirname(os.path.abspath(__file__))
current_path = os.path.dirname(os.path.abspath(__file__))

def loader_text(extension):
    ''' multiple files for *.txt or *.pdf using DirectoryLoader or PyPDFDirectoryLoaderusing'''
    ''' chunking before saving text into vector store'''
    ''' pip install pypdf for pdf file'''
    if extension == 'txt':

        loader = TextLoader(os.getcwd() + '/Data/test.txt', encoding="utf-8")
        data = loader.load()
        # print(data)
        
        '''
        text_loader_kwargs = {"autodetect_encoding": True}

        loader = DirectoryLoader(
            os.getcwd(),
            glob="**/*.txt",
            loader_cls=TextLoader,
            silent_errors=True,
            loader_kwargs=text_loader_kwargs,
        )
        '''
        data = loader.load()
       
    elif extension == 'pdf':
        loader = PyPDFLoader(os.getcwd() + "/Data/asiabrief_3-26.pdf")
        data = loader.load_and_split()
        # print(data)


    print('***')
    print(f'type : {type(data)} / len : {len(data)}')
    print(f'data : {data}')
    print(f'page_content : {data[0].page_content}')
    print('***')
    print('\n')
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=0)
    texts = text_splitter.split_documents(data)

    for i, text in enumerate(texts):
        print(f"{i} : {text.page_content}")


if __name__ == "__main__":
    ''' https://velog.io/@kingjiwoo/%EC%B0%B8%EC%A1%B0-%EB%AC%B8%EC%84%9C-%EA%B8%B0%EB%B0%98%EC%9C%BC%EB%A1%9C-LangChain-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B01 '''
    loader_text("txt")
    # loader_text("pdf")
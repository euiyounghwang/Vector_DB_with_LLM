
from langchain_community.document_loaders import TextLoader # type: ignore
from langchain_community.document_loaders import DirectoryLoader # type: ignore
from langchain.document_loaders import PyPDFLoader # type: ignore
from langchain_community.document_loaders import Docx2txtLoader # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
from langchain.text_splitter import CharacterTextSplitter # type: ignore
''' split characters  ["\n\n", "\n", " ", ""]'''
''' length_function , chunk_size , chunk_overlap, add_start_index (Determines whether to include the start position of the chunk within the original document in the metadata) '''

import json

import warnings
warnings.filterwarnings("ignore")
import os
os.environ['CURL_CA_BUNDLE'] = ''

# current_path = os.path.dirname(os.path.abspath(__file__))
current_path = os.path.dirname(os.path.abspath(__file__))

path = os.getcwd() + "/Data/"

def loader_text(input_file, create_json=False):
    ''' multiple files for *.txt or *.pdf using DirectoryLoader or PyPDFDirectoryLoaderusing'''
    ''' chunking before saving text into vector store'''

    content = []
    json_format = {"ES_UPLOADED" : "JSON_FORMAT"}

    _chunk_size = 200

    def extract_txt_file(input_file):
        loader = TextLoader(path + input_file, encoding="utf-8")
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

        return data
    

    def extract_pdf_file(input_file):
        ''' pip install pypdf for pdf file'''
        loader = PyPDFLoader(path + input_file)
        data = loader.load_and_split()
        # print(data)

        return data
    
    
    def extract_docx_file(input_file):
        ''' pip install docx2txt'''
        loader = Docx2txtLoader(path + input_file)
        data = loader.load_and_split()
        # print(data)

        return data
    
    def create_es_json_format(index_name, content):
        ''' make a json format for ES cluster'''
        actions = []
        print('\n')
        # print("Full context : {}".format('\n'.join(content)))

        actions.append({'index': {'_index': index_name, '_type' : "search"}})
        json_format.update({"CONTENT" : '\n'.join(content)})
        actions.append(json_format)

        print(json.dumps(actions, indent=2, ensure_ascii=False))

        # response = es_client.bulk(body=actions)
        # del actions[:]

    
    ''' Validate file extension if it does exist'''
    if not "." in str(input_file):
        data = extract_txt_file(input_file)
    else:
        extension = str(input_file).split(".")[1]
        
        if extension == 'pdf':
            data = extract_pdf_file(input_file)

        elif extension == 'docx':
            data = extract_docx_file(input_file)

        else:
            data = extract_txt_file(input_file)


    print('***')
    print(f'type : {type(data)} / len : {len(data)}')
    print(f'data : {data}')
    print(f'page_content : {data[0].page_content}')
    print('***')
    print('\n')
    
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=_chunk_size, chunk_overlap=0)
    text_splitter = CharacterTextSplitter(chunk_size=0,chunk_overlap=0, separator = '\n')
    texts = text_splitter.split_documents(data)

    for i, text in enumerate(texts):
        print(f"{i} : {text.page_content}")
        content.append(text.page_content)

    ''' any indexing into es'''
    create_es_json_format("test_context", content)


if __name__ == "__main__":
    ''' https://velog.io/@kingjiwoo/%EC%B0%B8%EC%A1%B0-%EB%AC%B8%EC%84%9C-%EA%B8%B0%EB%B0%98%EC%9C%BC%EB%A1%9C-LangChain-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B01 '''
    # loader_text("test.txt", create_json=True)
    # loader_text("asiabrief_3-26.pdf", create_json=True)
    loader_text("Sample.docx", create_json=True)
    # loader_text("test", create_json=True)
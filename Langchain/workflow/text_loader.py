
from typing import List
from langchain_community.document_loaders import TextLoader # type: ignore
from langchain_community.document_loaders import DirectoryLoader # type: ignore
# from langchain.document_loaders import PyPDFLoader # type: ignore
from langchain_community.document_loaders import PyPDFLoader # type: ignore
from langchain_community.document_loaders import Docx2txtLoader # type: ignore
from langchain_community.document_loaders import UnstructuredPowerPointLoader # type: ignore
from langchain_community.document_loaders import UnstructuredExcelLoader # type: ignore
from langchain_community.document_loaders import WebBaseLoader # type: ignore
from langchain_teddynote.document_loaders import HWPLoader # type: ignore
from langchain_core.documents import Document # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
from langchain.text_splitter import CharacterTextSplitter # type: ignore
from es_utils import util

''' split characters  ["\n\n", "\n", " ", ""]'''
''' length_function , chunk_size , chunk_overlap, add_start_index (Determines whether to include the start position of the chunk within the original document in the metadata) '''

''' https://python.langchain.com/docs/versions/v0_2/ '''

import json
import bs4
import re
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['CURL_CA_BUNDLE'] = ''

# current_path = os.path.dirname(os.path.abspath(__file__))
current_path = os.path.dirname(os.path.abspath(__file__))

path = os.getcwd() + "/Data/"



def process_pages(pages: List[Document]) -> List[Document]:
    return [Document(page_content=util.transform_trim_string(page.page_content), metadata=page.metadata) for page in pages]


def loader_text(input_file, create_json=False):
    ''' multiple files for *.txt or *.pdf using DirectoryLoader or PyPDFDirectoryLoaderusing'''
    ''' chunking before saving text into vector store'''

    content = []
    json_format = {"_source" : {"ES_UPLOADED" : "JSON_FORMAT"}}

    _chunk_size = 200

    def extract_txt_file(input_file):
        ''' https://python.langchain.com/v0.1/docs/modules/data_connection/document_loaders/ '''
        loader = TextLoader(input_file, encoding="utf-8")
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

        ''' preprocessing for Document '''
        data = process_pages(data)
        # print(data)

        return data
    
    def extract_web_url(input_file):
        ''' Need to check the element in html poge source'''
        loader = WebBaseLoader(
            web_paths=(input_file,),
            bs_kwargs=dict(
                parse_only=bs4.SoupStrainer(
                    "div",
                    attrs={"class": ["newsct_article _article_body", "media_end_head_title"]},
                )
            ),
            header_template={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
            },
        )
        data = loader.load()
        # print(data)

        return data
    

    def extract_pdf_file(input_file):
        ''' https://python.langchain.com/v0.2/docs/how_to/document_loader_pdf/ '''
        ''' pip install pypdf for pdf file'''
        loader = PyPDFLoader(input_file)
        data = loader.load_and_split()

        ''' preprocessing for Document '''
        data = process_pages(data)
        # print(data)

        return data
    
    
    def extract_docx_file(input_file):
        ''' https://python.langchain.com/docs/integrations/document_loaders/microsoft_word/ '''
        ''' pip install docx2txt'''
        loader = Docx2txtLoader(input_file)
        data = loader.load_and_split()

        ''' preprocessing for Document '''
        data = process_pages(data)
        # print(data)

        return data
    

    def extract_pptx_file(input_file):
        ''' pip install unstructured python-magic python-pptx '''
        loader = UnstructuredPowerPointLoader(input_file)
        data = loader.load()
        print(data)

        return data
    

    def extract_excel_file(input_file):
        ''' https://python.langchain.com/docs/integrations/document_loaders/microsoft_excel/ '''
        ''' pip install langchain-community unstructured openpyxl xlrd '''
        loader = UnstructuredExcelLoader(input_file, mode="elements")
        data = loader.load()

        ''' preprocessing for Document '''
        data = process_pages(data)
        print(data)

        return data
    

    def extract_hwp_file(input_file):
        ''' https://wikidocs.net/253708 '''
        ''' pip install langchain-teddynote '''
        loader = HWPLoader(input_file)
        data = loader.load()

        ''' preprocessing for Document '''
        data = process_pages(data)
        # print(data, type(data))

        return data
       
    

    def extract_text(input_file):
        ''' Tika: https://github.com/chrismattmann/tika-python '''
        ''' Extract text using tika library'''
        import tika # type: ignore
        from tika import parser # type: ignore
        parsed = parser.from_file(input_file)
        # print(parsed["metadata"])
        # print(parsed["content"])
        data = parsed["content"]

        ''' tranform to type(doc) : <class 'langchain_core.documents.base.Document'>'''
        ''' refering to https://hyundoil.tistory.com/295'''
        transform_lanchain = []
        for manual_paging, text in enumerate(data.split('\n')):
            if text:
                transform_lanchain.append(Document(page_content=str(text), metadata=dict(page=manual_paging)))

        ''' preprocessing for Document '''
        data = process_pages(transform_lanchain)

        return data
        

    def create_es_json_format(index_name, input_file, content):
        ''' make a json format for ES cluster'''
        actions = []
        print('\n')
        # print("Full context : {}".format('\n'.join(content)))

        actions.append({'index': {'_index': index_name, '_type' : "search"}})
        json_format.update({"_source" : {"CONTENT" : '\n'.join(content), "FILE" : input_file}})
        json_format.update({"_id" : "222"})
        actions.append(json_format)

        print(json.dumps(actions, indent=2, ensure_ascii=False))

        # response = es_client.bulk(body=actions)
        # del actions[:]

        return actions
    

    print(f'Loading {input_file}')

    ''' Validate file extension if it does exist'''
    if "http" in str(input_file):
        data = extract_web_url(input_file)
    elif not "." in str(input_file):
        data = extract_txt_file(input_file)
    else:
        print(f'File: {input_file}')

        split_extension = str(input_file).rsplit(".",1)
        print(f'split_extension: {split_extension}')
        extension =split_extension[1]
        print(f'extension: {extension}')
        
        if extension == 'pdf':
            data = extract_pdf_file(input_file)
            # data = extract_text(input_file)

        elif extension.startswith('doc'):
            data = extract_docx_file(input_file)
            # data = extract_text(input_file)

        elif extension.startswith('ppt'):
            # data = extract_pptx_file(input_file)
            data = extract_text(input_file)
            # return ""
        
        elif extension.startswith('xls'):
            data = extract_excel_file(input_file)
            # data = extract_text(input_file)

        elif extension.startswith('hwp'):
            data = extract_hwp_file(input_file)
            # data = extract_text(input_file)
        
        else:
            data = extract_txt_file(input_file)
            # data = extract_text(input_file)


    print('***')
    print(f'type : {type(data)} / len : {len(data)}')
    print(f'data : {data}')

    if not isinstance(data[0], (str, list)):
        print(f'page_content : {data[0].page_content}')
    print('***')
    print('\n')
    
    ''' split characters  ["\n\n", "\n", " ", ""]'''
    ''' length_function , chunk_size , chunk_overlap, add_start_index (Determines whether to include the start position of the chunk within the original document in the metadata) '''
    # text_splitter = RecursiveCharacterTextSplitter(chunk_size=_chunk_size, chunk_overlap=0)
    text_splitter = CharacterTextSplitter(chunk_size=0,chunk_overlap=0, separator = '\n')

    if not isinstance(data[0], (str)):
        texts = text_splitter.split_documents(data)
    else:
        texts = text_splitter.split_text(data)

    ''' return langchain document type'''
    if not create_json:
        print("\ntype(document)", type(texts))
        return texts
    
    for i, text in enumerate(texts):
        if not isinstance(data[0], (str)):
            print(f"{i} : {text.page_content}")
            content.append(text.page_content)
        else:
            content.append(data)

    ''' any indexing into es'''
    print(f"Progressing..")

    return create_es_json_format("test_context", input_file, content)
    
    


if __name__ == "__main__":
    ''' https://velog.io/@kingjiwoo/%EC%B0%B8%EC%A1%B0-%EB%AC%B8%EC%84%9C-%EA%B8%B0%EB%B0%98%EC%9C%BC%EB%A1%9C-LangChain-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B01 '''
    # loader_text("{}/{}".format(path, "test.txt"), create_json=True)
    # loader_text("{}/{}".format(path, "asiabrief_3-26.pdf"), create_json=True)
    # loader_text("{}/{}".format(path, "Sample.docx"), create_json=True)
    # loader_text("{}/{}".format(path, "Sample.doc"), create_json=True)
    # loader_text("{}/{}".format(path, "Sample.pptx"), create_json=True)
    # loader_text("{}/{}".format(path, "test"), create_json=True)
    # loader_text("{}/{}".format(path, "Sample.xls"), create_json=True)
    loader_text("{}/{}".format(path, "Sample.hwp"), create_json=True)
    # loader_text("https://n.news.naver.com/article/437/0000378416", create_json=True)
    
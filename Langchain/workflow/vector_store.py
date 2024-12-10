from langchain_core.documents import Document # type: ignore
from langchain_community.vectorstores import FAISS # type: ignore
from langchain_community.embeddings import HuggingFaceEmbeddings # type: ignore
from langchain_community.vectorstores import Chroma # type: ignore
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['CURL_CA_BUNDLE'] = ''
import shutil
import json
import pandas as pd

path = os.getcwd() + "/chroma_data"

class vector_store_faiss:

    def __init__(self):
        ''' type(doc) : <class 'langchain_core.documents.base.Document'> '''
        self.docs_for_test_embed = [
            Document(page_content="사과", metadata=dict(page=1)),
            Document(page_content="애플", metadata=dict(page=1)),
            Document(page_content="바나나", metadata=dict(page=2)),
            Document(page_content="오렌지", metadata=dict(page=2)),
            Document(page_content="고양이", metadata=dict(page=3)),
            Document(page_content="야옹", metadata=dict(page=3)),
            Document(page_content="강아지", metadata=dict(page=4)),
            Document(page_content="멍멍", metadata=dict(page=4)),
            Document(page_content="해", metadata=dict(page=5)),
            Document(page_content="달", metadata=dict(page=5)),
            Document(page_content="물", metadata=dict(page=6)),
            Document(page_content="불", metadata=dict(page=6)),
            Document(page_content="apple", metadata=dict(page=7)),
        ]
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/faiss_data"
        self.embeddings = HuggingFaceEmbeddings(
                model_name="BAAI/bge-m3",
                model_kwargs = {'device': 'cpu'}, # 모델이 CPU에서 실행되도록 설정. GPU를 사용할 수 있는 환경이라면 'cuda'로 설정할 수도 있음
                encode_kwargs = {'normalize_embeddings': True}, # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
        )
        self.database = FAISS.from_documents(self.docs_for_test_embed, self.embeddings)

        # if os.path.exists(self.path):
        #     shutil.rmtree(self.path)


    def similarity_search_with_score(self, keyword: str) -> None:
        ''' OpenAIEmbeddings, GoogleGenerativeAIEmbeddings, HuggingFaceEmbeddings, OllamaEmbeddings  '''
        print(f"type(docs_for_test_embed) : {type(self.docs_for_test_embed)}")
        results_with_scores = self.database.similarity_search_with_score(keyword, k=5)
        print(f"Keyword: {keyword}")
        for doc, score in results_with_scores:
            print(f"type(doc) : {type(doc)}")
            print(f" > Content: {doc.page_content} / Metadata: {doc.metadata} / Score: {score}({score:.10f})")
            # print(f" > Content: {doc} / Metadata: {doc} / Score: {score}({score:.10f})")


class vector_store_chroma:
    ''' https://hyundoil.tistory.com/295 '''

    def __init__(self, reset_db):
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/chroma_data"
        ''' initialize vector db'''
        self.initialize_db(reset_db)
        self.embeddings = HuggingFaceEmbeddings(
                model_name="BAAI/bge-m3",
                model_kwargs = {'device': 'cpu'}, 
                encode_kwargs = {'normalize_embeddings': True}, # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
        )

        ''' create chroma_data director with vector data'''
        self.database = Chroma(persist_directory=self.path, embedding_function = self.embeddings)
        
    
    def initialize_db(self, reset_db):
        if reset_db:
            if os.path.exists(self.path):
                shutil.rmtree(self.path)

    
    def similarity_search_with_score(self, input_list: list) -> None:
        ''' OpenAIEmbeddings, GoogleGenerativeAIEmbeddings, HuggingFaceEmbeddings, OllamaEmbeddings  '''
        ind = self.database.add_texts(input_list)
        print("similarity_search_with_score : {}".format(ind))


    def get_vector_store_chroma(self):
        print('get_vector_store_chroma : {}'.format(json.dumps(self.database.get(), indent=2, ensure_ascii=False)))
        print('\n')
        data = self.database.get()
        data = pd.DataFrame(data)
        print(data.head())

        return self.database.get()
        


if __name__ == "__main__":
    ''' pip install faiss-cpu or pip install faiss-gpu'''
    ''' pip install requests==2.27.1 '''
    '''
    python ./Langchain/vector_store.py
    
    Keyword: 사과
    > Content: 사과 / Metadata: {'page': 1} / Score: 0.0(0.0000000000)
    > Content: apple / Metadata: {'page': 7} / Score: 0.9053352475166321(0.9053352475)
    > Content: 애플 / Metadata: {'page': 1} / Score: 0.962782621383667(0.9627826214)
    > Content: 바나나 / Metadata: {'page': 2} / Score: 1.0399245023727417(1.0399245024)
    > Content: 고양이 / Metadata: {'page': 3} / Score: 1.0497236251831055(1.0497236252)
    Keyword: 강아지
    > Content: 강아지 / Metadata: {'page': 4} / Score: 0.0(0.0000000000)
    > Content: 고양이 / Metadata: {'page': 3} / Score: 0.42204996943473816(0.4220499694)
    > Content: 야옹 / Metadata: {'page': 3} / Score: 0.8820641040802002(0.8820641041)
    > Content: 멍멍 / Metadata: {'page': 4} / Score: 0.9173198938369751(0.9173198938)
    > Content: 오렌지 / Metadata: {'page': 2} / Score: 0.9445515871047974(0.9445515871)
    Keyword: 해
    > Content: 해 / Metadata: {'page': 5} / Score: 7.433983983951009e-13(0.0000000000)
    > Content: 달 / Metadata: {'page': 5} / Score: 0.9844512939453125(0.9844512939)
    > Content: 물 / Metadata: {'page': 6} / Score: 0.9882267713546753(0.9882267714)
    > Content: 사과 / Metadata: {'page': 1} / Score: 1.0772922039031982(1.0772922039)
    > Content: apple / Metadata: {'page': 7} / Score: 1.087688684463501(1.0876886845)
    
    (.venv)
    '''
    try:
        # faiss_vector_store = vector_store_faiss()
        # faiss_vector_store.similarity_search_with_score("사과")
        # faiss_vector_store.similarity_search_with_score("강아지")
        # faiss_vector_store.similarity_search_with_score("해")

        ''' chroma'''
        chroma_vector_store = vector_store_chroma(reset_db=False)
        input_list = ['test 데이터 입력1', 'test 데이터 입력2']
        # chroma_vector_store.similarity_search_with_score(input_list)
        chroma_vector_store.get_vector_store_chroma()

    except Exception as e:
        print(e)
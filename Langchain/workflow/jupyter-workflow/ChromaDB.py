from langchain_community.vectorstores import FAISS # type: ignore
from langchain_community.embeddings import HuggingFaceEmbeddings # type: ignore
from langchain_community.vectorstores import Chroma # type: ignore
from langchain_community.vectorstores import FAISS # type: ignore
from langchain_core.documents import Document # type: ignore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions
import chromadb
from chromadb.config import Settings
import json
import uuid
import os, sys
import tiktoken
import warnings
warnings.filterwarnings("ignore")

# -- pip install requests==2.27.1 
os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''

class MySentenceEmbedding():
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs = {'device': 'cpu'}, # 모델이 CPU에서 실행되도록 설정. GPU를 사용할 수 있는 환경이라면 'cuda'로 설정할 수도 있음
            encode_kwargs = {'normalize_embeddings': True}, # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
        )
        # self.default_embeddings = embedding_functions.DefaultEmbeddingFunction()
        
    def get_sentence_embedding(self, docs):
        embed = self.embeddings.embed_documents(docs)
        # embed = self.default_embeddings(docs)
        print(f"len(embed): {len(embed)}")
        # print(f"embed : {embed}")
        return embed
    

def work():
    chroma_client = chromadb.HttpClient(host="localhost", port=8000)
    chroma_client.heartbeat()

    try:
        print(chroma_client.list_collections()) # collection 목록 가져오기

        collection = chroma_client.get_or_create_collection(name="new_collection")
        print(f"get_or_create_collection : {collection.peek()}")
        
    #     collection = chroma_client.get_collection("new_collection")
    #     print(collection.peek())
        
        print(f"chroma_client.list_collections() : {chroma_client.list_collections()}")

        collection_count = chroma_client.count_collections()
        print(f"collection_count : {collection_count}")

        # rst = MySentenceEmbedding().get_sentence_embedding(["Love is wanting to be loved", "test"])
        # print(rst)

        documents=[
            "This is a document about pineapple",
            # "This is a document about oranges",
            # "This is a document about apples",
            # "I'm JeongTae Park"
        ]

        ids = [str(uuid.uuid4()) for i in range(len(documents))]
        print(f"ids : {ids}")

        metadatas = [
            {"index": i, "version": 1.0} for i in range(len(documents))
        ]

        print(f"metadata : {metadatas}")

        # embeddings = [
        #     MySentenceEmbedding().get_sentence_embedding([document]) for document in documents
        # ]
        embeddings = MySentenceEmbedding().get_sentence_embedding(documents)

        # Chroma will store your text and handle embedding and indexing automatically. 
        # You can also customize the embedding model. You must provide unique string IDs for your documents.
        # https://docs.trychroma.com/docs/overview/getting-started
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids = ids
        )

        collection = chroma_client.get_collection("new_collection")
        print(collection.peek())

    except Exception as e:
        print(str(e))

    finally:
        print("Done..")


if __name__ == "__main__":
    work()
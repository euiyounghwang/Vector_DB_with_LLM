
from langchain_community.embeddings import HuggingFaceEmbeddings # type: ignore
import warnings
warnings.filterwarnings("ignore")
import os
os.environ['CURL_CA_BUNDLE'] = ''


def embedding():
    ''' OpenAIEmbeddings, GoogleGenerativeAIEmbeddings, HuggingFaceEmbeddings, OllamaEmbeddings  '''
    embeddings = HuggingFaceEmbeddings(
        model_name="BAAI/bge-m3",
        model_kwargs = {'device': 'cpu'}, # 모델이 CPU에서 실행되도록 설정. GPU를 사용할 수 있는 환경이라면 'cuda'로 설정할 수도 있음
        encode_kwargs = {'normalize_embeddings': True}, # 임베딩 정규화. 모든 벡터가 같은 범위의 값을 갖도록 함. 유사도 계산 시 일관성을 높여줌
    )
    embed = embeddings.embed_documents(
        [
            "안녕 영광",
            "동해물과 백두산",
            "마르고 닳도록",
            "하느님이 보우하사",
            "우리나라 만세"
        ]
    )
    print(f"len(embed): {len(embed)}")
    print(f"len(embed[0]): {len(embed[0])}")
    print(f"len(embed[1]): {len(embed[1])}")
    # print(f"embed: {embed}")


if __name__ == "__main__":
    ''' pip install sentence-transformers '''
    ''' pip install requests==2.27.1 '''
    '''
     python ./Langchain/embedding.py
    len(embed): 5
    len(embed[0]): 1024
    len(embed[1]): 1024
    '''
    embedding()
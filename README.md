# Vector_DB_with_LLM
Vector_DB_with_LLM

LangChain(https://github.com/langchain-ai/langchain) is a framework for developing applications powered by large language models (LLMs). LangChain is an open source framework for building applications based on large language models (LLMs). LLMs are large deep-learning models pre-trained on large amounts of data that can generate responses to user queries. for example, answering questions or creating images from text-based prompts. Prompts are queries people use to seek responses from an LLM.
- Example : https://colab.research.google.com/github/i-am-shuan/learn-langchain/blob/main/langchain_RAG_example.ipynb

VectorDB (i.e, Milvus, Faiss (Facebook AI Similarity Search), Chroma, Qdrant, Pinecone) : A Vector Database (VectorDB) is designed to store and manage vector data, often used in machine learning and AI applications. Vector data refers to numerical representations of objects, which can be used for similarity search, clustering, and other tasks. (Reference : https://krishna-yogik.medium.com/vectordb-tutorial-a-beginners-guide-06dc333fac2f)
- Use Cases of VectorDB
    - Recommendations System: Powering personalized recommendations by finding similar users or items based on their vector representations. (Examples: Movie, music, or product recommendations)
    - Image and Video Retrieval: Enabling content-based image and video retrieval by searching for similar visual features.
    - Natural Language Processing (NLP): Finding semantically similar texts, documents, or queries using vector embeddings from models like BERT or Word2Vec. (Examples: Document clustering, sentiment analysis, semantic search)
    - Anomaly Detection: Identifying unusual patterns or outliers in high-dimensional data. (Fraud detection, network intrusion detection)


### Using Poetry: Create the virtual environment in the same directory as the project and install the dependencies:
- Gunicorn/FastAPI : https://chaechae.life/blog/fastapi-deployment-gunicorn#google_vignette
```bash
python -m venv .venv
source .venv/bin/activate
pip install poetry

# --
poetry config virtualenvs.in-project true
pip install poetry
poetry init
poetry add openai langchain langchainhub tiktoken chromadb langchain-community bs4 python-dotenv
```

#### Python V3.9 Install
```bash
pip install --q openai langchain langchainhub tiktoken chromadb langchain-community bs4

# when error occur like this
# ImportError: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168
pip install urllib3==1.26.18
pip install pytz
```


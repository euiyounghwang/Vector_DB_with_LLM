# Vector_DB_with_LLM
Vector_DB_with_LLM

LangChain(https://github.com/langchain-ai/langchain) is a framework for developing applications powered by large language models (LLMs). LangChain is an open source framework for building applications based on large language models (LLMs). LLMs are large deep-learning models pre-trained on large amounts of data that can generate responses to user queries. for example, answering questions or creating images from text-based prompts. Prompts are queries people use to seek responses from an LLM.
- Example : https://colab.research.google.com/github/i-am-shuan/learn-langchain/blob/main/langchain_RAG_example.ipynb, https://velog.io/@kwon0koang/%EB%A1%9C%EC%BB%AC%EC%97%90%EC%84%9C-Llama3-%EB%8F%8C%EB%A6%AC%EA%B8%B0
- Documentation : https://wikidocs.net/231600
- Artical: https://hackernoon.com/lang/ko/ollama-python-%EB%B0%8Fchromdb%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EB%A1%9C%EC%BB%AC%EC%97%90%EC%84%9C-LLM%EC%9D%84-%EC%84%A4%EC%A0%95%ED%95%98%EB%8A%94-%EB%8B%A8%EA%B3%84%EB%B3%84-%EA%B0%80%EC%9D%B4%EB%93%9C%EB%A1%9C-%EB%82%98%EB%A7%8C%EC%9D%98-%EB%9E%98%EA%B7%B8-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0
- Local LLM : https://github.com/firstpersoncode/local-rag?ref=hackernoon.com


VectorDB (i.e, Milvus, Faiss (Facebook AI Similarity Search), Chroma, Qdrant, Pinecone) : A Vector Database (VectorDB) is designed to store and manage vector data, often used in machine learning and AI applications. Vector data refers to numerical representations of objects, which can be used for similarity search, clustering, and other tasks. (Reference : https://krishna-yogik.medium.com/vectordb-tutorial-a-beginners-guide-06dc333fac2f)
- Use Cases of VectorDB
    - Recommendations System: Powering personalized recommendations by finding similar users or items based on their vector representations. (Examples: Movie, music, or product recommendations)
    - Image and Video Retrieval: Enabling content-based image and video retrieval by searching for similar visual features.
    - Natural Language Processing (NLP): Finding semantically similar texts, documents, or queries using vector embeddings from models like BERT or Word2Vec. (Examples: Document clustering, sentiment analysis, semantic search)
    - Anomaly Detection: Identifying unusual patterns or outliers in high-dimensional data. (Fraud detection, network intrusion detection)


RAG(Retrieval Augemented Generation) is an AI technique that allows companies to automatically embed their most current and relevant proprietary data directly into their LLM prompt.
- We’re not just talking about structured data like a spreadsheet or a relational database.
- We mean retrieving all available data, including unstructured data: emails, PDFs, chat logs, social media posts, and other types of information that could lead to a better AI output.
- In a nutshell, RAG helps companies retrieve and use their data from various internal sources for better generative AI results. 
- To achieve this improved accuracy, RAG works in conjunction with a specialized type of database — called a vector database — to store data in a numeric format that makes sense for AI, and retrieve it when prompted.
- RAG can’t do its job without the vector database doing its job.V
- Step (https://blog.naver.com/htk1019/223442628204) : Document Loader ⮕ Text Splitter ⮕ Embedding ⮕ Vector Store (Saving vector) ⮕ Retriver


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

### Python V3.9 Install
```bash
pip install --q openai langchain langchainhub tiktoken chromadb langchain-community bs4

# when error occur like this
# ImportError: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168
pip install urllib3==1.26.18
pip install pytz
```


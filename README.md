# Vector_DB_with_LLM
<i>Vector_DB_with_LLM


FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python.
This is a repository that provides to deliver the records to the Prometheus-Export application.

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

Streamlit is an open-source Python framework for data scientists and AI/ML engineers to deliver interactive data apps
- https://github.com/streamlit/llm-examples, https://pypi.org/project/streamlit-chat/
- Streamlit Install & Run
```bash
pip install streamlit 
pip install streamlit-chat

streamlit run [streamlit-filenam.py] [--server.port 30001]
streamlit run app.py
```
- App testing : https://github.com/streamlit/llm-examples/blob/main/.github/workflows/app-testing.yml
- requirements-dev.txt
```bash
black==23.3.0
mypy==1.4.1
pre-commit==3.3.3
watchdog
pytest
```
- Codespaces (https://github.com/features/codespaces, https://velog.io/@profile_exe/Github-Codespaces): GitHub Codespaces gets you up and coding faster with fully configured, secure cloud development environments native to GitHub.


#### Python V3.9 Install
- Gunicorn/FastAPI : https://chaechae.life/blog/fastapi-deployment-gunicorn#google_vignette
- Python3.11 with Openssl (https://datamoney.tistory.com/378)
```bash
sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel git 
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz 
tar –zxvf Python-3.9.0.tgz or tar -xvf Python-3.9.0.tgz 
cd Python-3.9.0 
./configure --libdir=/usr/lib64 
sudo make 
sudo make altinstall 

# python3 -m venv .venv --without-pip
sudo yum install python3-pip

sudo ln -s /usr/lib64/python3.9/lib-dynload/ /usr/local/lib/python3.9/lib-dynload

# -- From Python ^3.10 , It need to be installed openssl
# openssl
cd /usr/local/src
wget https://www.openssl.org/source/openssl-1.1.1t.tar.gz
tar xvf openssl-1.1.1t.tar.gz

cd openssl-1.1.1t/
./config --prefix=/usr/local/ssl --openssldir=/usr/local/ssl shared zlib
make
sudo make install

export LDFLAGS="-L/usr/local/ssl/lib"
export CPPFLAGS="-I/usr/local/ssl/include"

# openssl확인
/usr/local/ssl/bin/openssl version
export LD_LIBRARY_PATH=/usr/local/ssl/lib:$LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH  


sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel git 
wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz 
tar –zxvf Python-3.11.0.tgz or tar -xvf Python-3.11.0.tgz 
cd Python-3.11.0 

# --with-openssl-rpath=auto 옵션을 추가하여 파이썬이 자동으로 올바른 OpenSSL 라이브러리 경로를 찾도록 함
# ./configure --libdir=/usr/lib64 --with-openssl=/usr/local/ssl --with-openssl-rpath=auto
./configure --libdir=/usr/lib64 --with-openssl=/usr/bin/ssl --with-openssl-rpath=auto
sudo make 
sudo make altinstall 

# -- Error occurs when installing packages via pip like below
(.venv) -bash-4.2$ pip install elasticsearch==7.13
WARNING: pip is configured with locations that require TLS/SSL, however the ssl module in Python is not available.
WARNING: Retrying (Retry(total=4, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/elasticsearch/
WARNING: Retrying (Retry(total=3, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError("Can't connect to HTTPS URL because the SSL module is not available.")': /simple/elasticsearch/
ERROR: Operation cancelled by user

#--


python -m venv .venv
source .venv/bin/activate

# -- Swagger
pip install poetry
poetry add fastapi
poetry add uvicorn
poetry add gunicorn
poetry add pytz
poetry add httpx
poetry add pytest
poetry add pytest-cov
poetry add requests
poetry add pyyaml
poetry add elasticsearch==7.13
poetry add python-dotenv


# --
# -- Vector
poetry config virtualenvs.in-project true
pip install poetry
poetry init
poetry add openai langchain langchainhub tiktoken chromadb langchain-community bs4 python-dotenv
poetry add sentence-transformers
poetry add pypdf
poetry add docx2txt
poetry add faiss-cpu
poetry add requests

pip install --q openai langchain langchainhub tiktoken chromadb langchain-community bs4

# when error occur like this
# ImportError: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168
pip install urllib3==1.26.18
pip install pytz
pip install requests==2.27.1
```


### Pytest
- Go to virtual enviroment using `source .venv/bin/activate`
- Run this command manually: `poetry run py.test -v --junitxml=test-reports/junit/pytest.xml --cov-report html --cov tests/` or `./pytest.sh`
```bash
$ ./pytest.sh
tests\test_api.py::test_skip SKIPPED (no way of currently testing this)                                                                                                                                                                                                                                           [ 50%]
tests\test_api.py::test_api PASSED                                                                                                                                                                                                                                                                                [100%]

---------- coverage: platform win32, python 3.11.7-final-0 -----------
Name                               Stmts   Miss  Cover   Missing
----------------------------------------------------------------
config\config.py                       8      4    50%   16-20, 33
config\log_config.py                  32      1    97%   42
controller\__init__.py                 0      0   100%
controller\cluster_controller.py      14      0   100%
injector.py                           25      0   100%
main.py                               23      9    61%   38-57, 69
service\__init__.py                    0      0   100%
service\es_search_handler.py         139    103    26%   32-88, 131-132, 139-155, 160-173, 178-191, 196-213, 219-254, 259-271, 276-287, 292-304, 309-315
service\es_util.py                    21     16    24%   5-11, 16-19, 24-35, 40-41
service\query_builder.py              42     27    36%   21-40, 48-51, 64-83, 89-98, 102-137
service\status_handler.py             13      2    85%   12, 19
tests\__init__.py                      0      0   100%
tests\conftest.py                      8      0   100%
tests\test_api.py                      9      1    89%   7
----------------------------------------------------------------
TOTAL                                334    163    51%

$
```


### CI/CD Environment
- CircleCI (`./circleci/config.yml`): CircleCI is a continuous integration and continuous delivery platform that helps software teams work smarter, faster. With CircleCI, every commit kicks off a new job in our platform, and code is built, tested, and deployed. 
- Github Actions (`./.github/workflows/build-and-test.yml`) : GitHub Actions is a continuous integration and continuous delivery (CI/CD) platform that allows you to automate your build, test, and deployment pipeline. You can create workflows that build and test every pull request to your repository, or deploy merged pull requests to production.



### Register Service
- sudo service vector_interface_api status/stop/start/restart
```bash
#-- /etc/systemd/system/vector_interface_api.service
[Unit]
Description=Swagger ES Service

[Service]
User=devuser
Group=devuser
Type=simple
ExecStart=/bin/bash /home/devuser/Git_Repo/service-start.sh
ExecStop= /usr/bin/killall vector_interface_api

[Install]
WantedBy=default.target


# Service command
sudo systemctl daemon-reload 
sudo systemctl start vector_interface_api.service 
sudo systemctl status vector_interface_api.service 
sudo systemctl stop vector_interface_api.service 

sudo service vector_interface_api status/stop/start
```
</i>

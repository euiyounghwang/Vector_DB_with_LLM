# Vector_DB_with_LLM
Vector_DB_with_LLM

LangChain(https://github.com/langchain-ai/langchain) is a framework for developing applications powered by large language models (LLMs). LangChain is an open source framework for building applications based on large language models (LLMs). LLMs are large deep-learning models pre-trained on large amounts of data that can generate responses to user queries. for example, answering questions or creating images from text-based prompts. Prompts are queries people use to seek responses from an LLM.
- Example : https://colab.research.google.com/github/i-am-shuan/learn-langchain/blob/main/langchain_RAG_example.ipynb



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


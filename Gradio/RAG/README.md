Auto-RAG via Gradio

- Reference : https://github.com/nsrinidhibhat/gradio_RAG/tree/main

This repository contains code and resources related to Retrieval Augmented Generation (RAG), a technique designed to address the data freshness problem in Large Language Models (LLMs) like Llama-2. LLMs often lack awareness of recent events and up-to-date information. RAG incorporates external knowledge from a knowledge base into LLM responses, enabling accurate and well-grounded responses.

RAG is a novel approach combining Large Language Models (LLMs) capabilities with external knowledge bases to enhance the quality and freshness of generated responses. It addresses the challenge of outdated information by retrieving contextually relevant knowledge from external sources and incorporating it into LLM-generated content.

Gradio is a Python library that helps you quickly create UIs for your machine learning models. It allows you to quickly deploy models and make them accessible through a user-friendly interface without extensive frontend development.

A Gradio app is launched when gradio_chatbot.py code is run. It contains modifiable elements such as the Embedding model, Generation model, editable system prompt, and tunable parameters of the chosen LLM.
FROM jupyter/datascience-notebook:latest AS analyzer
RUN pip install -qU "langchain[openai]"
RUN pip install -U langchain-community
RUN pip install numpy==1.26.4
RUN pip install pypdf unstructured python-docx langchain-chroma
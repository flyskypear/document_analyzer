import glob
import os
import pandas as pd
from time import sleep
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, UnstructuredWordDocumentLoader
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

class DocumentAnalyzer:

    def __init__(self, model, api_key, api_url, text_model, 
                chunk_size=1000, chunk_overlap=100, num_chunks=10, 
                persist_directory="chroma_db", temperature=0):
        self.model = model
        self.api_key = api_key
        self.api_url = api_url
        self.embedding_model = text_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.num_chunks = num_chunks
        self.persist_directory = persist_directory
        self.temperature = temperature

    def vectorstore_exists(self):
        # check if the vectorstore already exists in the given directory
        if os.path.exists(self.persist_directory):
            print(f"Vectorstore already exists at {self.persist_directory}.")
            return True
        return False

    def get_file_paths(self, directory):
        search_pattern = os.path.join(directory, '**', '*')
        file_paths = glob.glob(search_pattern, recursive=True)
        file_paths = [path for path in file_paths if os.path.isfile(path)]
        return file_paths

    # parse .xlxs files 
    def _load_excel_as_documents(self, file_path: str):
        dfs = pd.read_excel(file_path, sheet_name=None) # dict: {sheet_name: DataFrame}
        docs = []
        for sheet_name, df in dfs.items():
            text = df.to_csv(index=False)
            metadata = {"source": file_path, "sheet_name": sheet_name}
            docs.append(Document(page_content=text, metadata=metadata))
        return docs

    def parse_files(self, files):
        # parse all the files and store the `Document` objects returned in a list
        documents = []
        for file_path in files:
            ext = os.path.splitext(file_path)[1].lower()
            docs = []
            if ext == ".pdf":
                loader = PyPDFLoader(file_path)
                docs = loader.load()
            elif ext == ".docx":
                loader = UnstructuredWordDocumentLoader(file_path)
                docs = loader.load()
            elif ext == ".csv":
                csv_loader = CSVLoader(file_path=file_path)
                docs = csv_loader.load()
            elif ext == ".xlsx":
                docs = self._load_excel_as_documents(file_path)
            else:
                print("missed")
            documents.extend(docs)
        return documents
    
    def create_vectorstore(self):
        # make the embedding function with the embedding model
        embedding_function = OpenAIEmbeddings(model=self.embedding_model, openai_api_key=self.api_key, 
                                              openai_api_base=self.api_url)
        # make a vector database to store all the embeddings 
        vectorstore = Chroma(
            collection_name="my_collection",
            embedding_function=embedding_function,
            persist_directory=self.persist_directory
        )
        return vectorstore
    
    def add_documents(self, documents, vectorstore, batch_size=20, wait_time=3):
        # separate a given text into 2000 sized chunks where each chunkoverlaps by 100
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        # split the files into chunks and store all the chunks as `Document` objects 
        split_docs = []
        for doc in documents:
            chunks = text_splitter.split_text(doc.page_content)
            for chunk in chunks:
                split_docs.append(
                    Document(page_content=chunk, metadata=doc.metadata)
                )
        # add 20 documents at a time to the database, each document will first be converted into embeddings 
        # by the embedding model and then added to the database. 
        for i in range(0, len(split_docs), batch_size):
            batch = split_docs[i : i + batch_size]
            vectorstore.add_documents(batch)
            # sleep to prevent too many requests error from the embedding model server 
            sleep(wait_time)
        

    def get_qa_chain(self, vectorstore, num_chunks=10):
        # make retriever object which would pick "k" (in this case 10) chunks for each query to the llm model
        retriever = vectorstore.as_retriever(search_kwargs={"k": num_chunks})
        # make the question-answer chain object
        qa_chain = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model_name=self.model, temperature=self.temperature, openai_api_key=self.api_key, 
                           openai_api_base=self.api_url),
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        return qa_chain


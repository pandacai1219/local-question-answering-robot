from langchain import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.document_loaders import UnstructuredPDFLoader
from keys import OpenAI_API_KEY
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from template import prompt_template_Document, prompt_template_GPT
import faiss
import pickle
from typing import Any

class FaissDB_Utils:
    def __init__(self, api_key=None,prompt_template=None,temperature=None,max_context_tokens=None,max_response_tokens=None,file_chunk_size=None):
        if api_key is None:
            self.api_key = OpenAI_API_KEY
        else:
            self.api_key = api_key
        if file_chunk_size is None:
            self.file_chunk_size = 200
        else:
            self.file_chunk_size = file_chunk_size
        if temperature is None:
            self.temperature = 0
        else:
            self.temperature = temperature
        if max_context_tokens is None:
            self.max_context_tokens = -1
        else:
            self.max_context_tokens = max_context_tokens
        if prompt_template is None:
            self.prompt_template = prompt_template_Document
        else:
            self.prompt_template = prompt_template
        print(f"self.prompt_template：{self.prompt_template}")
        print(f"self.temperature：{self.temperature}")
        print(f"self.max_context_tokens：{self.max_context_tokens}")
        print(f"self.file_chunk_size：{self.file_chunk_size}")
        print(f"self.api_key：{self.api_key}")
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.api_key)
        self.text_splitter = CharacterTextSplitter(chunk_size=self.file_chunk_size, chunk_overlap=0)
        self.llm = OpenAI(temperature=self.temperature, max_tokens=self.max_context_tokens, openai_api_key=self.api_key)
        PROMPT = PromptTemplate(template=self.prompt_template, input_variables=["context", "question"])
        print(str(PROMPT))
        self.chain = load_qa_chain(llm=self.llm, chain_type='stuff', verbose=True, prompt=PROMPT)
        self.docCount = 0

    def create_or_import_to_db(self, file_path, filename=None,userName=None):
        db = None
        folder_path="dbf/"+userName
        print(f"folder_path：{folder_path}")
        # 根据文件类型加载文档
        if file_path.endswith(".docx") or file_path.endswith(".doc"):
            loader = UnstructuredWordDocumentLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
        elif file_path.endswith(".pdf"):
            loader = UnstructuredPDFLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

        documents = loader.load()
        print(str(documents))
        docs = self.text_splitter.split_documents(documents)

        print(f"Found {len(docs)} documents in {file_path}")
        self.docCount=len(docs)
        db_local=None
        try:
            db_local = FAISS.load_local(index_name=userName, embeddings=self.embeddings, folder_path=folder_path)

            for doc in docs:
                doc_temp = [doc]
                db_temp = FAISS.from_documents(documents=doc_temp, embedding=self.embeddings)
                db_local.merge_from(db_temp)

            db_local.save_local(folder_path=folder_path, index_name=userName)
        except Exception as e:
            db = FAISS.from_documents(documents=docs, embedding=self.embeddings)
            db.save_local(folder_path=folder_path, index_name=userName)
            print(f"Error loading db: {e}")


        print(f"Saved db to {filename}{userName}")

    def get_document_by_vector_id(vector_id):
        with open("index.pkl", "rb") as f:
            docstore, index_to_docstore_id = pickle.load(f)
        docstore_id = index_to_docstore_id[vector_id]
        metadata = docstore[docstore_id]
        return metadata

    def search_documents(self, query, userName=None):
        folder_path="dbf/"+userName
        print(f"folder_path：{folder_path}")

        db = FAISS.load_local(index_name=userName,embeddings=self.embeddings,folder_path=folder_path)

        results  = db.similarity_search(query, k=3)

        return results
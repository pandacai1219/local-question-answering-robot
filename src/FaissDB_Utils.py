from langchain import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredWordDocumentLoader
from keys import OpenAI_API_KEY
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

class FaissDB_Utils:
    def __init__(self, api_key=None,prompt_template=None,temperature=None,max_context_tokens=None,max_response_tokens=None,file_chunk_size=None):
        if api_key is None:
            self.api_key = OpenAI_API_KEY
        else:
            self.api_key = api_key
        if file_chunk_size is None:
            self.file_chunk_size = file_chunk_size
        else:
            self.file_chunk_size = 100
        self.max_context_tokens = max_context_tokens
        self.temperature=temperature
        self.embeddings = OpenAIEmbeddings(openai_api_key=OpenAI_API_KEY)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.file_chunk_size, chunk_overlap=20)
        self.llm = OpenAI(temperature=self.temperature, max_tokens=self.max_context_tokens, openai_api_key=self.api_key)
        PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        print(str(PROMPT))
        self.chain = load_qa_chain(llm=self.llm, chain_type='stuff', verbose=True, prompt=PROMPT)
        self.docCount = 0


    def create_or_import_to_db(self, file_path, persist_directory=None,userName=None):
        db = None
        folder_path="dbf/"+userName
        print(f"folder_path：{folder_path}")
        try:
           db = FAISS.load_local(index_name=persist_directory,embeddings=self.embeddings,folder_path=folder_path)
        except Exception as e:
            print(f"Error loading db: {e}")
        # 根据文件类型加载文档
        if file_path.endswith(".docx") or file_path.endswith(".doc"):
            loader = UnstructuredWordDocumentLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file format: {file_path}")

        documents = loader.load()
        print(str(documents))
        docs = self.text_splitter.split_documents(documents)

        print(f"Found {len(docs)} documents in {file_path}")
        self.docCount=len(docs)

        # 将文档导入数据库
        db = FAISS.from_documents(docs, self.embeddings)
        #通过将文本块的嵌入表示传递给FAISS类的from_texts方法，创建FAISS向量存储对象。
        #store = FAISS.from_texts(docs, self.embeddings)

        # 保存 FAISS 索引
        db.save_local(index_name=persist_directory,folder_path=folder_path)
        print(f"Saved db to {persist_directory}{userName}")

    def search_documents(self, query, persist_directory=None,userName=None):
        folder_path="dbf/"+userName
        print(f"folder_path：{folder_path}")

        db = FAISS.load_local(index_name=persist_directory,embeddings=self.embeddings,folder_path=folder_path)

        results  = db.similarity_search(query, k=3, fetch_k=10)

        return results
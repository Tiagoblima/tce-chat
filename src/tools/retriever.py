
import asyncio
import bs4
from langchain import hub
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import DataFrameLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings, HuggingFaceBgeEmbeddings, HuggingFaceInstructEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_cohere import CohereRerank
import torch

class BaseRetriever:

    embeddings = None


    def start(self, model_name: str = "BAAI/bge-m3", device: str = 'cpu', normalize_embeddings: bool = True):
        # Load the embeddings model
        model_kwargs = {'device': device}
        encode_kwargs = {'normalize_embeddings': normalize_embeddings}
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name=model_name,
            model_kwargs=model_kwargs,
            encode_kwargs=encode_kwargs
        )
        return self.embeddings
        

    def create_retriever(self):

        embeddings = self.start()
        index_name = "tce-pe-idx"
        vectorstore = PineconeVectorStore(index_name=index_name, embedding=embeddings )
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 25})
        return self.retriever

    
class Retriever(BaseRetriever):

    def __init__(self):
        super().__init__()
        self.loop = asyncio.get_event_loop()
        self.start()
        self.create_retriever()
        self.retriever = self.create_retriever()
        
    async def get_retriever(self, prompt: str, llm):

        compressor = await CohereRerank(model="rerank-multilingual-v3.0")
       

        base_retriever = self.create_retriever()

        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=base_retriever
        )

        history_aware_retriever = create_history_aware_retriever(
            llm, compression_retriever, prompt
        )
        
        return history_aware_retriever

    def get_embeddings(self):
        return self.embeddings
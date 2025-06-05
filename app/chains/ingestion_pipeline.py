# Process the ingestion and uploading of documents to the vectorstore
from app.loaders.github_loader import GithubRepoLoader
from app.processing.chunk_splitter import DocumentProcessor
from app.db.pinecone_db import VectorStore
from app.models.LLM import LLMChat
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import asyncio

class IngestionPipeline:
    def __init__(self,github_repo_loader:GithubRepoLoader, document_processor:DocumentProcessor, vector_store:VectorStore ):
        self.github_repo_loader = github_repo_loader
        self.document_processor = document_processor
        self.vector_store = vector_store
    async def ingest_github_repo(self, repo_name: str, branch: str="master", filter_file_extension:str=None):
        documents = await self.github_repo_loader.load_github_docs(repo_name=repo_name, branch=branch, filter_file_extension=filter_file_extension)
        print(f"Downloaded {len(documents)} documents from github.")
        splited_documents = await self.document_processor.document_splitter(documents)
        print(f"Splited into {len(splited_documents)} document chunks.")
        print("Embedding...")
        await self.vector_store.add_documents(splited_documents[:3])
        print("done!")
        return len(splited_documents)
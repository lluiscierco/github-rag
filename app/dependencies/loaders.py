# Fastapi dependencies
from fastapi import Depends
from app.loaders.github_loader import GithubRepoLoader
from app.processing.chunk_splitter import DocumentProcessor
from app.db.pinecone_db import VectorStore
from app.llm.LLM import LLMClient
from app.chains.ingestion_pipeline import IngestionPipeline
from app.chains.rag_chain import RagChain

_github_repo_loader_instance: GithubRepoLoader | None = None
def get_github_repo_loader() -> GithubRepoLoader:
    global _github_repo_loader_instance
    if _github_repo_loader_instance is None:
        _github_repo_loader_instance = GithubRepoLoader()
    return _github_repo_loader_instance


_document_processor_instance: DocumentProcessor | None = None
def get_document_processor() -> DocumentProcessor:
    global _document_processor_instance
    if _document_processor_instance is None:
        _document_processor_instance = DocumentProcessor()
    return _document_processor_instance


_vector_store_instance: VectorStore | None = None
def get_vector_store() -> VectorStore:
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = VectorStore()
    return _vector_store_instance

_llm_client_instance: LLMClient | None = None
def get_llm_client() -> LLMClient:
    global _llm_client_instance
    if _llm_client_instance is None:
        _llm_client_instance = LLMClient()
    return _llm_client_instance

def get_ingestion_pipeline(
    github_repo_loader=Depends(get_github_repo_loader),
    document_processor=Depends(get_document_processor),
    vector_store=Depends(get_vector_store),
):
    return IngestionPipeline(
        github_repo_loader=github_repo_loader,
        document_processor=document_processor,
        vector_store=vector_store,
    )

def get_rag_pipeline(
    vector_store=Depends(get_vector_store),
    llm_client=Depends(get_llm_client)
):
    return RagChain(
        vector_store=vector_store,
        llm_client=llm_client
    )
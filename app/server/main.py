# Create fast api server
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from app.loaders.github_loader import GithubRepoLoader
from app.processing.chunk_splitter import DocumentProcessor
from app.db.pinecone_db import VectorStore
from app.models.LLM import LLMChat
from app.chains.ingestion_pipeline import IngestionPipeline
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import asyncio

app = FastAPI()

# Fastapi dependencies
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

# -- API calls --
from pydantic import BaseModel
from typing import Optional, List

class IngestRequest(BaseModel):
    repo_name: str
    branch: str
    filter_file_extension: Optional[List[str]] = None

@app.post("/ingest_github_repo/")
async def ingest_github_repo_endpoint(request:IngestRequest, ingestion_pipeline: IngestionPipeline = Depends(get_ingestion_pipeline)):
    """
    Endpoint to trigger the ingestion of a GitHub repository into the vector store.
    """
    repo_name= request.repo_name
    branch=request.branch
    filter_file_extension=request.filter_file_extension
    #"langchain-ai/langchain"
    try:
        if filter_file_extension is None:
            filter_file_extension = [".md"]
        chunk_len = await ingestion_pipeline.ingest_github_repo(repo_name=repo_name, branch=branch, filter_file_extension=filter_file_extension)
        return {"message": f"Ingestion successful. {chunk_len} chunks uploaded to the vector store",
                "cunck lenght": chunk_len}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ingestion failed: {str(e)}")


async def call_chain():
    vector_store = VectorStore()
    retriever = vector_store.as_retriever()
    llmchat = LLMChat()
    llm = llmchat.llm
    prompt = llmchat.prompt_template
    rag_chain = (
        RunnableMap(
            {
                "context": retriever | llmchat.build_context,
                "question": RunnablePassthrough(),
            }
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    response = await rag_chain.ainvoke("Can i use this project in a devcontainer?")
    print(response)

# Add a root endpoint for health checks
@app.get("/")
async def root():
    return {"message": "RAG Backend is running. Use /ingest-github-repo or /query-rag."}

#uvicorn app.server.main:app --reload


# Create fast api server
from fastapi import FastAPI, Depends, HTTPException, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.dependencies.loaders import get_ingestion_pipeline, get_rag_pipeline
from app.chains.rag_chain import RagChain
from app.chains.ingestion_pipeline import IngestionPipeline
from app.models.schema import IngestRequest, RAGRequest
import asyncio
import logging
from .logger import setup_logging
app = FastAPI()

# --- NEW: Add CORS middleware ---
# This allows your frontend (running on a different port or domain)
# to communicate with your backend.
origins = [
    "https://git-rag-app.onrender.com"
    #"http://localhost",
    #"http://localhost:8080",
    #"http://127.0.0.1:5500", # Common port for VS Code Live Server
    #"null", # Allows opening the HTML file directly (origin: "null")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)

# Initialize logging during startup
@app.on_event("startup")
async def startup_event():
    setup_logging()
    logging.getLogger(__name__).info("🚀 FastAPI application has started.")

# -- API calls --
@app.post("/ingest_github_repo/")
async def ingest_github_repo_endpoint(
    request: IngestRequest,
    ingestion_pipeline: IngestionPipeline = Depends(get_ingestion_pipeline),
):
    """
    Endpoint to trigger the ingestion of a GitHub repository into the vector store.
    """
    repo_name = request.repo_name # "pydantic/pydantic"
    branch = request.branch
    filter_file_extension = request.filter_file_extension
    chunk_size = request.chunk_size
    chunk_overlap = request.chunk_overlap
    splitter = request.splitter
    
    try:
        chunk_len = await ingestion_pipeline.ingest_github_repo(
            repo_name=repo_name,
            branch=branch,
            filter_file_extension=filter_file_extension,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            splitter=splitter,
        )
        return {
            "message": f"Ingestion successful. {chunk_len} chunks uploaded to the vector store",
            "cunck lenght": chunk_len,
        }
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ingestion failed: {str(e)}",
        )


@app.post("/query-rag/")
async def ingest_github_repo_endpoint(
    request: RAGRequest, rag_chain: RagChain = Depends(get_rag_pipeline)
):
    """
    Endpoint to trigger the ingestion of a GitHub repository into the vector store.
    """
    question = request.question
    try:
        answer = await rag_chain.run(question=question)
        return {"message": "RAG answering successful.", "Answer": answer}
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG failed: {str(e)}",
        )


# Add a root endpoint for health checks
@app.get("/")
async def root():
    return {"message": "RAG Backend is running. Use /ingest-github-repo or /query-rag."}


# uvicorn app.main:app --reload

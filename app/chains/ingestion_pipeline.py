# Process the ingestion and uploading of documents to the vectorstore
from app.loaders.github_loader import GithubRepoLoader
from app.processing.chunk_splitter import DocumentProcessor
from app.db.pinecone_db import VectorStore
from app.models.schema import SplitterType
import logging

logger = logging.getLogger(__name__)


class IngestionPipeline:
    def __init__(
        self,
        github_repo_loader: GithubRepoLoader,
        document_processor: DocumentProcessor,
        vector_store: VectorStore,
    ):
        self.github_repo_loader = github_repo_loader
        self.document_processor = document_processor
        self.vector_store = vector_store

    async def ingest_github_repo(
        self,
        repo_name: str,
        branch: str,
        filter_file_extension: list[str] | None,
        splitter: SplitterType,
        chunk_size: int,
        chunk_overlap: int,
    ):
        logger.info(f"Get files from repo: {repo_name}, branch: {branch}.")
        documents = await self.github_repo_loader.load_github_docs(
            repo_name=repo_name,
            branch=branch,
            filter_file_extension=filter_file_extension,
        )
        logger.info(f"Downloaded {len(documents)} documents from github.")
        splited_documents = await self.document_processor.document_splitter(
            documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            splitter=splitter,
        )
        logger.info(f"Splited into {len(splited_documents)} document chunks.")
        logger.info("Uploading to vector store...")
        await self.vector_store.add_documents(splited_documents)
        logger.info("done!")
        return len(splited_documents)

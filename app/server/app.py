# Create fast api server
from app.loaders.github_loader import load_github_docs
from app.processing.chunk_splitter import document_splitter
from app.models.embeddings import document_embedder
from app.db.pinecone_db import VectorStore

def test_end_to_end():
    documents = load_github_docs(repo_name="langchain-ai/langchain")
    print(f"Downloaded {len(documents)} documents from github.")
    splited_documents = document_splitter(documents)
    print(f"Splited into {len(splited_documents)} document chunks.")
    print("Embedding...")
    vector_store = VectorStore()
    vector_store.add_documents(splited_documents[:3])
    print("done!")

if __name__ == "__main__":
    test_end_to_end()
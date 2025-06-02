# Create fast api server
from app.loaders.github_loader import load_github_docs
from app.processing.chunk_splitter import document_splitter
from app.models.embeddings import document_embedder

def test_end_to_end():
    documents = load_github_docs(repo_name="langchain-ai/langchain")
    print(f"Downloaded {len(documents)} documents from github.")
    splited_documents = document_splitter(documents)
    print(f"Splited into {len(splited_documents)} document chunks.")
    print("Embedding...")
    #embeded_documents = document_embedder(splited_documents[:3])
    #print(embeded_documents[0])

if __name__ == "__main__":
    test_end_to_end()
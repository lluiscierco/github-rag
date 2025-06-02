# Create fast api server
from app.loaders.github_loader import load_github_docs
from app.processing.chunk_splitter import document_splitter
from app.db.pinecone_db import VectorStore
from app.models.LLM import LLMChat

def test_end_to_end():
    documents = load_github_docs(repo_name="langchain-ai/langchain")
    print(f"Downloaded {len(documents)} documents from github.")
    splited_documents = document_splitter(documents)
    print(f"Splited into {len(splited_documents)} document chunks.")
    print("Embedding...")
    vector_store = VectorStore()
    vector_store.add_documents(splited_documents[:3])
    print("done!")
def test_retrival():
    vector_store = VectorStore()
    retrived_docs = vector_store.retrive_context(query="Can i use this project in a devcontainer?")
    #print(retrived_docs)
    llm = LLMChat()
    answer = llm.invoke("Can i use this project in a devcontainer?", retrived_docs[0][0].page_content)
    print(answer)
    

if __name__ == "__main__":
    #test_end_to_end()
    test_retrival()
# Create fast api server
from app.loaders.github_loader import load_github_docs
from app.processing.chunk_splitter import document_splitter
from app.db.pinecone_db import VectorStore
from app.models.LLM import LLMChat
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def test_end_to_end():
    documents = load_github_docs(repo_name="langchain-ai/langchain")
    print(f"Downloaded {len(documents)} documents from github.")
    splited_documents = document_splitter(documents)
    print(f"Splited into {len(splited_documents)} document chunks.")
    print("Embedding...")
    vector_store = VectorStore()
    vector_store.add_documents(splited_documents[:3])
    print("done!")
def call_chain():
    vector_store = VectorStore()
    retriever = vector_store.as_retriever()
    llmchat=LLMChat()
    llm = llmchat.llm
    prompt=llmchat.prompt_template
    rag_chain = (
            RunnableMap({
                "context": retriever | llmchat.build_context,
                "question": RunnablePassthrough()
            })
            | prompt
            | llm
            | StrOutputParser()
        )
    response = rag_chain.invoke("Can i use this project in a devcontainer?")
    print(response)

if __name__ == "__main__":
    #test_end_to_end()
    call_chain()
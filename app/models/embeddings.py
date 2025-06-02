# Embedding model
# from langchain_community.embeddings import HuggingFaceEndpointEmbeddings #HuggingFaceInferenceAPIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from app import config

HUGGINGFACE_KEY = config.HUGGINGFACE_KEY


def document_embedder(documents):
    embeddings = HuggingFaceEndpointEmbeddings(
        huggingfacehub_api_token=HUGGINGFACE_KEY,
        model="sentence-transformers/all-mpnet-base-v2",
    )
    texts = [doc.page_content for doc in documents]

    embedded_documents = embeddings.embed_documents(texts)
    return embedded_documents

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from app import config


class VectorStore:
    def __init__(self):
        self.HUGGINGFACE_KEY = config.HUGGINGFACE_KEY
        self.PC_KEY = config.PC_KEY
        self.PC_INDEX = config.PC_INDEX
        self.embeddings = HuggingFaceEndpointEmbeddings(
            huggingfacehub_api_token=self.HUGGINGFACE_KEY,
            model="sentence-transformers/all-mpnet-base-v2",
        )
        self.vector_store = self._connect_vector_store()

    def _connect_vector_store(self):
        pc = Pinecone(api_key=self.PC_KEY)
        index = pc.Index(host=self.PC_INDEX)
        vector_store = PineconeVectorStore(embedding=self.embeddings, index=index)
        return vector_store

    def add_documents(self, documents: list):
        custom_ids = [doc.metadata['id'] for doc in documents]
        return self.vector_store.add_documents(documents, ids=custom_ids)

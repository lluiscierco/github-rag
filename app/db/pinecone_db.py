from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from app import config
import asyncio

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

    async def add_documents(self, documents: list):
        custom_ids = [doc.metadata["id"] for doc in documents]
        return await self.vector_store.aadd_documents(documents, ids=custom_ids)

    def as_retriever(self, top_k: int = 4, score_threshold: float = 0.5):
        return self.vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"k": top_k, "score_threshold": score_threshold},
        )

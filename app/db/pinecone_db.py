from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from app import config
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # <-- Super slow! We can only make a request once every 10 seconds!!
    check_every_n_seconds=0.1,  # Wake up every 100 ms to check whether allowed to make a request,
    max_bucket_size=10,  # Controls the maximum burst size.
)

class VectorStore:
    def __init__(self):
        self.HUGGINGFACE_KEY = config.HUGGINGFACE_KEY
        self.PC_KEY = config.PC_KEY
        self.PC_INDEX = config.PC_INDEX
        """
        self.embeddings = HuggingFaceEndpointEmbeddings(
            huggingfacehub_api_token=self.HUGGINGFACE_KEY,
            model="sentence-transformers/all-mpnet-base-v2",
        )
        """
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
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

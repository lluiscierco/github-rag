# Create the full process pipeline
from app.db.pinecone_db import VectorStore
from app.llm.LLM import LLMClient
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

import logging

logger = logging.getLogger(__name__)

class RagChain:
    def __init__(self, vector_store:VectorStore, llm_client:LLMClient):
        self.vector_store = vector_store
        self.retriever = self.vector_store.as_retriever()
        self.llm_client = llm_client
        self.llm = llm_client.llm
        self.prompt = llm_client.prompt_template
        self.rag_chain = (
            RunnableMap(
                {
                    "context": self.retriever | self.llm_client.build_context,
                    "question": RunnablePassthrough(),
                }
            )
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    async def run(self, question:str) -> str:
        logger.info("Runing rag chain...")
        answer = await self.rag_chain.ainvoke(question)
        logger.info(f"Answer: {answer}")
        return answer
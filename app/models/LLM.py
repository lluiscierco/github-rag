from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate
from app import config

GOOGLE_API_KEY = config.GOOGLE_API_KEY

class LLMChat:
    def __init__(self):
        self.llm = init_chat_model("gemini-2.5-flash-preview-05-20", model_provider="google_genai")
        self.prompt_template = PromptTemplate(
            input_variables=["question", "context"],
            template=(
                "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. "
                "If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\n"
                "Question: {question}\n"
                "Context: {context}\n"
                "Answer:"
            )
        )
    
    def build_context(self, relevants_docs: list) -> str:
        context = "\n\n".join(doc.page_content for doc in relevants_docs)
        return context

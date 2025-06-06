# Split the docs in chunks of text
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.models.schema import SplitterType
class DocumentProcessor:
    def __init__(self):
        pass
    def _create_text_splitter(self, splitter:SplitterType, chunk_size: int, chunk_overlap: int):
        if splitter == "recursive_character":
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                length_function=len,
                is_separator_regex=False,
            )
            return text_splitter
        else:
            raise ValueError(f"Unsupported splitter type: {splitter}")
    async def document_splitter(self,documents: list, splitter: SplitterType="recursive_character", chunk_size:int = 1000, chunk_overlap:int = 100) -> list:
        """
        Split a list of documents into smaller text sizes. Docs mantain the original metadata

        Args:
            documents (_type_): list of langchain documents
            chunk_size (int, optional): Lenght of each chunk. Defaults to 1000.
            chunk_overlap (int, optional): Lenght of the overlap between consecutive chunks. Defaults to 100.

        Returns:
            _type_: List of documents
        """
        text_splitter = self._create_text_splitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            splitter=splitter
        )
        
        splited_documents = await text_splitter.atransform_documents(documents)

        # Add custom IDs
        for i, chunk in enumerate(splited_documents):
            sha = chunk.metadata.get("sha", "unknown")
            chunk.metadata["id"] = f"{sha}-chunk-{i}"

        return splited_documents
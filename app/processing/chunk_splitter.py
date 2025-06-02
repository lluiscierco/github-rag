# Split the docs in chunks of text
from langchain_text_splitters import RecursiveCharacterTextSplitter

def document_splitter(documents: list, chunk_size:int = 1000, chunk_overlap:int = 100) -> list:
    """
    Split a list of documents into smaller text sizes. Docs mantain the original metadata

    Args:
        documents (_type_): list of langchain documents
        chunk_size (int, optional): Lenght of each chunk. Defaults to 1000.
        chunk_overlap (int, optional): Lenght of the overlap between consecutive chunks. Defaults to 100.

    Returns:
        _type_: List of documents
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    splited_documents = text_splitter.split_documents(documents)

    return splited_documents
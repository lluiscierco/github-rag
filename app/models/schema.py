from pydantic import BaseModel
from typing import Optional, List
from typing import Literal

SplitterType = Literal["recursive_character"]

class IngestRequest(BaseModel):
    repo_name: str
    branch: str = "main"
    filter_file_extension: list[str] | None = None
    chunk_size: int = 1000
    chunk_overlap: int = 100
    splitter: SplitterType = "recursive_character"

class RAGRequest(BaseModel):
    question: str
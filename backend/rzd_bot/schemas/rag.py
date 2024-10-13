from typing import List, Dict

from pydantic import BaseModel, Field

from .documents import BranchEnum


class QuestionRequest(BaseModel):
    question: str
    branch: BranchEnum = None
    docs_ids: List[str] = None
    user_profile: str = ""


class Document(BaseModel):
    content: str
    metadata: Dict[str, str]


class RAGResponse(BaseModel):
    answer: str
    small_answer: str
    docs: List[Document]

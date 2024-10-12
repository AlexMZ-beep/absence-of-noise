from typing import List, Dict

from pydantic import BaseModel

from .documents import BranchEnum


class QuestionRequest(BaseModel):
    question: str
    branch: BranchEnum = BranchEnum.ALL
    user_profile: str = ""


class Document(BaseModel):
    content: str
    metadata: Dict[str, str]


class RAGResponse(BaseModel):
    answer: str
    small_answer: str
    docs: List[Document]

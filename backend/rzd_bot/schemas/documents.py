from enum import Enum

from fastapi import File, UploadFile
from pydantic import BaseModel, Field


class BranchEnum(str, Enum):
    ALL = "ALL"
    A = "A"
    B = "B"
    C = "C"


class DocumentResponse(BaseModel):
    id: str
    title: str
    branch: BranchEnum = None


class DocumentCreate(BaseModel):
    title: str = Field(..., description="Название документа")
    file: UploadFile = File(..., description="PDF файл для загрузки")
    branch: BranchEnum = Field(..., description="Филиал")

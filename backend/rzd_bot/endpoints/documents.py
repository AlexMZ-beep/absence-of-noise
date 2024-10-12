from fastapi import APIRouter, status, HTTPException, UploadFile, File, Form
from typing import List

import rzd_bot.utils.documents as docs_utils

from rzd_bot.schemas import DocumentResponse, BranchEnum

api_router = APIRouter(tags=["Documents"])


@api_router.post(
    "/docs",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Загрузить новый документ",
    description="Эндпоинт для загрузки документа в базу данных."
)
async def upload_document(
    title: str = Form(..., description="Название документа"),
    branch: BranchEnum = Form(..., description="Филиал"),
    file: UploadFile = File(..., description="PDF файл для загрузки")
):
    """
    Загрузка нового документа.
    - **document**: Данные документа для загрузки.
    """
    try:
        file_content = await file.read()
        new_doc = docs_utils.upload_document(file_content, title, branch)
        return new_doc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при загрузке документа: {str(e)}"
        )


@api_router.delete(
    "/documents/{doc_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить существующий документ",
    description="Эндпоинт для удаления документа по его ID."
)
async def delete_document(doc_id: str):
    """
    Удаление документа по ID.

    - **doc_id**: Идентификатор документа для удаления.
    """
    try:
        success = docs_utils.delete_document(doc_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Документ не найден."
            )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при удалении документа: {str(e)}"
        )


@api_router.get(
    "/documents",
    response_model=List[DocumentResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список документов",
    description="Эндпоинт для получения списка всех документов в базе данных."
)
async def get_list_documents():
    """
    Получение списка всех документов.
    """
    documents = docs_utils.get_documents()
    return documents

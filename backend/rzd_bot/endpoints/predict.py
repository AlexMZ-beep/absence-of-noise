from fastapi import APIRouter, status

from rzd_bot.schemas import QuestionRequest, RAGResponse
from rzd_bot.utils.chains import chain_with_formated_output

api_router = APIRouter(tags=["RAG"])


@api_router.post(
    "/predict",
    response_model=RAGResponse,
    status_code=status.HTTP_200_OK,
)
async def predict(question_data: QuestionRequest):
    answer = await chain_with_formated_output.ainvoke(question_data.dict())
    return RAGResponse(**answer)

from fastapi import APIRouter, status

from rzd_bot.schemas import QuestionRequest, RAGResponse
from rzd_bot.utils.chains import chain_with_formated_output
from rzd_bot.utils.common import save_logs

api_router = APIRouter(tags=["RAG"])


@api_router.post(
    "/predict",
    response_model=RAGResponse,
    status_code=status.HTTP_200_OK,
)
async def predict(question_data: QuestionRequest):
    answer = await chain_with_formated_output.ainvoke(question_data.dict())
    save_logs(question_data.dict(), answer)

    return RAGResponse(**answer)

from fastapi import APIRouter, status

from rzd_bot.schemas import PingResponse

api_router = APIRouter(tags=["Health check"])


@api_router.get(
    "/health_check/ping",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return PingResponse()

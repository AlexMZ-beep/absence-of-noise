from .health_check import api_router as health_check_router
from .predict import api_router as rag_router
from .documents import api_router as documents_router

list_of_routes = [
    health_check_router,
    rag_router,
    documents_router,
]

list_of_langserve_routes = []

__all__ = [
    "list_of_routes",
    "list_of_langserve_routes",
]

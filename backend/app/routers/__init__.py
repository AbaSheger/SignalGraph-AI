from app.routers.workspaces import router as workspaces_router
from app.routers.documents import router as documents_router
from app.routers.query import router as query_router
from app.routers.dashboard import router as dashboard_router

__all__ = ["workspaces_router", "documents_router", "query_router", "dashboard_router"]

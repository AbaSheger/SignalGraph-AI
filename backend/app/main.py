from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import workspaces_router, documents_router, query_router, dashboard_router
from app.database import init_db

app = FastAPI(
    title="SignalGraph AI",
    description="Agentic RAG assistant for engineering operations",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workspaces_router)
app.include_router(documents_router)
app.include_router(query_router)
app.include_router(dashboard_router)


@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/health")
async def health():
    return {"status": "ok"}

import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.workspace import Workspace
from app.schemas.query import QueryRequest, QueryResponse, Citation
from app.schemas.investigation import InvestigationRequest, InvestigationResponse
from app.services.retrieval import retrieve_chunks
from app.services.similarity import find_similar_incidents
from app.services.investigation import run_investigation
from app.services.embedding import embed_texts, cosine_similarity
from app.services.llm import MockLlmService
from app.config import settings

router = APIRouter(prefix="/workspaces", tags=["query"])


def _check_workspace(ws) -> None:
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")


@router.post("/{workspace_id}/ask", response_model=QueryResponse)
async def ask_question(
    workspace_id: uuid.UUID,
    body: QueryRequest,
    db: AsyncSession = Depends(get_db),
):
    ws = await db.get(Workspace, workspace_id)
    _check_workspace(ws)

    chunks = await retrieve_chunks(db, workspace_id, body.query)
    query_vec = embed_texts([body.query])[0]

    citations: list[Citation] = []
    for c in chunks:
        score = cosine_similarity(query_vec, c.get("embedding") or [])
        citations.append(Citation(
            source=c["filename"],
            chunk_index=c["chunk_index"],
            score=round(score, 4),
            excerpt=c["content"][:200],
        ))

    llm = MockLlmService()
    result = llm.generate_answer(body.query, chunks, [ci.model_dump() for ci in citations])
    return QueryResponse(
        answer=result["answer"],
        confidence=result["confidence"],
        citations=citations,
        missing_evidence=result["missing_evidence"],
    )


@router.post("/{workspace_id}/investigate", response_model=InvestigationResponse)
async def investigate(
    workspace_id: uuid.UUID,
    body: InvestigationRequest,
    db: AsyncSession = Depends(get_db),
):
    ws = await db.get(Workspace, workspace_id)
    _check_workspace(ws)
    return await run_investigation(db, workspace_id, body.query)


@router.post("/{workspace_id}/similar-incidents")
async def similar_incidents(
    workspace_id: uuid.UUID,
    body: QueryRequest,
    db: AsyncSession = Depends(get_db),
):
    ws = await db.get(Workspace, workspace_id)
    _check_workspace(ws)
    results = await find_similar_incidents(db, workspace_id, body.query)
    return {"results": results}

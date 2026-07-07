from __future__ import annotations

import uuid
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.models.document import Document
from app.services.embedding import embed_texts, cosine_similarity
from app.config import settings


async def retrieve_chunks(
    db: AsyncSession,
    workspace_id: uuid.UUID,
    query: str,
    k: int | None = None,
) -> list[dict]:
    """Return the top-k chunks ranked by cosine similarity to the query."""
    k = k or settings.max_chunks_retrieved
    query_vec = embed_texts([query])[0]

    # Try pgvector cosine search; fall back to in-memory for SQLite (tests)
    try:
        stmt = (
            select(
                Chunk.id,
                Chunk.content,
                Chunk.chunk_index,
                Chunk.embedding,
                Chunk.metadata_,
                Document.filename,
                Document.id.label("document_id"),
            )
            .join(Document, Chunk.document_id == Document.id)
            .where(Chunk.workspace_id == workspace_id)
            .where(Chunk.embedding.isnot(None))
            .order_by(
                text(
                    "embedding <=> CAST(:vec AS vector)"
                ).bindparams(vec=str(query_vec))
            )
            .limit(k)
        )
        rows = (await db.execute(stmt)).all()
    except Exception:
        # Fallback: load all chunks and rank in Python
        rows = await _fallback_retrieve(db, workspace_id, query_vec, k)

    return [_row_to_dict(row) for row in rows]


async def _fallback_retrieve(
    db: AsyncSession,
    workspace_id: uuid.UUID,
    query_vec: list[float],
    k: int,
) -> list:
    stmt = (
        select(
            Chunk.id,
            Chunk.content,
            Chunk.chunk_index,
            Chunk.embedding,
            Chunk.metadata_,
            Document.filename,
            Document.id.label("document_id"),
        )
        .join(Document, Chunk.document_id == Document.id)
        .where(Chunk.workspace_id == workspace_id)
        .where(Chunk.embedding.isnot(None))
    )
    rows = (await db.execute(stmt)).all()
    scored = sorted(
        rows,
        key=lambda r: cosine_similarity(query_vec, r.embedding),
        reverse=True,
    )
    return scored[:k]


def _row_to_dict(row) -> dict:
    score = row.embedding  # placeholder; actual score computed elsewhere
    return {
        "chunk_id": str(row.id),
        "document_id": str(row.document_id),
        "filename": row.filename,
        "chunk_index": row.chunk_index,
        "content": row.content,
        "score": 0.0,  # populated by caller when needed
        "metadata": row.metadata_ or {},
    }

from __future__ import annotations

import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chunk import Chunk
from app.models.document import Document
from app.models.entity import Entity
from app.services.embedding import embed_texts, cosine_similarity
from app.config import settings


async def find_similar_incidents(
    db: AsyncSession,
    workspace_id: uuid.UUID,
    text_snippet: str,
    k: int | None = None,
) -> list[dict]:
    """Return the top-k similar incidents for the given text snippet."""
    k = k or settings.max_chunks_retrieved
    query_vec = embed_texts([text_snippet])[0]

    # Fetch all chunks with embeddings
    stmt = (
        select(
            Chunk.id,
            Chunk.content,
            Chunk.chunk_index,
            Chunk.embedding,
            Chunk.document_id,
            Document.filename,
        )
        .join(Document, Chunk.document_id == Document.id)
        .where(Chunk.workspace_id == workspace_id)
        .where(Chunk.embedding.isnot(None))
    )
    rows = (await db.execute(stmt)).all()

    # Score each chunk
    scored = sorted(
        [
            {
                "document_id": str(r.document_id),
                "filename": r.filename,
                "chunk_index": r.chunk_index,
                "content": r.content,
                "score": cosine_similarity(query_vec, r.embedding),
            }
            for r in rows
        ],
        key=lambda x: x["score"],
        reverse=True,
    )

    # Deduplicate to one result per document, keep best score
    seen: set[str] = set()
    top: list[dict] = []
    for item in scored:
        doc_id = item["document_id"]
        if doc_id not in seen:
            seen.add(doc_id)
            top.append(item)
        if len(top) >= k:
            break

    # Enrich with entity data
    results = []
    for item in top:
        entity_stmt = select(Entity).where(
            Entity.document_id == uuid.UUID(item["document_id"])
        )
        entity = (await db.execute(entity_stmt)).scalars().first()
        results.append(
            {
                "document_id": item["document_id"],
                "filename": item["filename"],
                "score": round(item["score"], 4),
                "service_name": entity.service_name if entity else None,
                "root_cause": entity.root_cause if entity else None,
                "fix_or_workaround": entity.fix_or_workaround if entity else None,
                "related_runbook": entity.related_runbook if entity else None,
                "excerpt": item["content"][:300],
            }
        )
    return results

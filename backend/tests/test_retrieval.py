import pytest
import uuid
from app.models.workspace import Workspace
from app.models.document import Document
from app.models.chunk import Chunk
from app.services.retrieval import retrieve_chunks
from app.services.embedding import embed_texts


@pytest.mark.asyncio
async def test_retrieve_chunks_empty(db):
    ws = Workspace(name="retrieval-ws")
    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    results = await retrieve_chunks(db, ws.id, "database timeout")
    assert results == []


@pytest.mark.asyncio
async def test_retrieve_chunks_with_data(db):
    ws = Workspace(name="retrieval-ws-2")
    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    doc = Document(
        workspace_id=ws.id,
        filename="test.md",
        doc_type="incident",
        content="database connection pool exhaustion",
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    texts = [
        "database connection pool exhaustion causes timeouts",
        "the payment api service is down",
    ]
    vecs = embed_texts(texts)
    for i, (text, vec) in enumerate(zip(texts, vecs)):
        chunk = Chunk(
            document_id=doc.id,
            workspace_id=ws.id,
            content=text,
            chunk_index=i,
            embedding=vec,
        )
        db.add(chunk)
    await db.commit()

    results = await retrieve_chunks(db, ws.id, "database timeout", k=2)
    assert len(results) >= 1
    assert all("content" in r for r in results)
    assert all("filename" in r for r in results)

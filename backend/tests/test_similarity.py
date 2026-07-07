import pytest
import uuid
from app.models.workspace import Workspace
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.entity import Entity
from app.services.similarity import find_similar_incidents
from app.services.embedding import embed_texts


@pytest.mark.asyncio
async def test_find_similar_incidents_empty(db):
    ws = Workspace(name="sim-ws-empty")
    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    results = await find_similar_incidents(db, ws.id, "payment api timeout")
    assert results == []


@pytest.mark.asyncio
async def test_find_similar_incidents_returns_results(db):
    ws = Workspace(name="sim-ws-2")
    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    doc = Document(
        workspace_id=ws.id,
        filename="payment-api-timeout.md",
        doc_type="incident",
        content="payment api timeout due to connection pool exhaustion",
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    text = "payment api timeout due to connection pool exhaustion"
    vec = embed_texts([text])[0]
    chunk = Chunk(
        document_id=doc.id,
        workspace_id=ws.id,
        content=text,
        chunk_index=0,
        embedding=vec,
    )
    db.add(chunk)

    entity = Entity(
        document_id=doc.id,
        workspace_id=ws.id,
        service_name="payment-api",
        error_type="ConnectionTimeout",
        severity="high",
        root_cause="connection pool exhaustion",
        fix_or_workaround="increase pool size",
        related_runbook="deployment-rollback-runbook.md",
    )
    db.add(entity)
    await db.commit()

    results = await find_similar_incidents(db, ws.id, "payment api connection timeout")
    assert len(results) >= 1
    top = results[0]
    assert top["filename"] == "payment-api-timeout.md"
    assert top["service_name"] == "payment-api"
    assert isinstance(top["score"], float)


@pytest.mark.asyncio
async def test_similarity_score_ordering(db):
    ws = Workspace(name="sim-ws-order")
    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    texts = [
        "database connection pool exhaustion",
        "unrelated topic about css styling",
    ]
    docs_created = []
    for t in texts:
        doc = Document(
            workspace_id=ws.id,
            filename=f"doc-{t[:10]}.md",
            doc_type="incident",
            content=t,
        )
        db.add(doc)
        await db.commit()
        await db.refresh(doc)
        vec = embed_texts([t])[0]
        chunk = Chunk(
            document_id=doc.id,
            workspace_id=ws.id,
            content=t,
            chunk_index=0,
            embedding=vec,
        )
        db.add(chunk)
        docs_created.append(doc)
    await db.commit()

    results = await find_similar_incidents(db, ws.id, "database connection exhaustion")
    assert len(results) >= 2
    # Most similar should have a higher score
    assert results[0]["score"] >= results[-1]["score"]

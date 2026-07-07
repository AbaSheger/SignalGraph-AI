import pytest
from app.services.investigation import classify_query, run_investigation
from app.models.workspace import Workspace
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.entity import Entity
from app.services.embedding import embed_texts


def test_classify_incident():
    assert classify_query("ConnectionTimeout error in payment service") == "incident"


def test_classify_log():
    assert classify_query("Traceback at line 42") == "log"


def test_classify_question():
    assert classify_query("How do I configure the connection pool?") == "question"


@pytest.mark.asyncio
async def test_run_investigation_empty_workspace(db):
    ws = Workspace(name="inv-ws-empty")
    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    response = await run_investigation(db, ws.id, "database connection pool exhaustion")
    assert response.query_type in ("incident", "question", "log")
    assert len(response.steps) == 5
    assert isinstance(response.answer, str)
    assert 0.0 <= response.confidence <= 1.0


@pytest.mark.asyncio
async def test_run_investigation_with_data(db):
    ws = Workspace(name="inv-ws-data")
    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    text = "payment api timeout due to connection pool exhaustion fix: increase pool size"
    doc = Document(
        workspace_id=ws.id,
        filename="payment-api-timeout.md",
        doc_type="incident",
        content=text,
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

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
        root_cause="connection pool exhaustion",
        fix_or_workaround="increase pool size",
    )
    db.add(entity)
    await db.commit()

    response = await run_investigation(db, ws.id, "payment api timeout")
    assert len(response.similar_incidents) >= 1
    assert response.confidence > 0.0
    assert len(response.citations) >= 1

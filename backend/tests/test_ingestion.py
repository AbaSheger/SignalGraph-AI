import pytest
from app.utils.text_processing import parse_file_content, detect_doc_type, chunk_text, strip_markdown
from app.services.ingestion import ingest_file


def test_parse_markdown():
    content = parse_file_content("incident.md", b"# Incident\nThis is a test.")
    assert "Incident" in content


def test_parse_json():
    content = parse_file_content("log.json", b'{"error": "timeout", "service": "api"}')
    assert "timeout" in content


def test_detect_doc_type_runbook():
    assert detect_doc_type("deployment-rollback-runbook.md", "rollback procedure") == "runbook"


def test_detect_doc_type_incident():
    assert detect_doc_type("outage.md", "incident severity critical root cause") == "incident"


def test_detect_doc_type_postmortem():
    assert detect_doc_type("postmortem.md", "postmortem timeline") == "postmortem"


def test_chunk_text_basic():
    text = " ".join([f"word{i}" for i in range(100)])
    chunks = chunk_text(text, chunk_size=20, overlap=5)
    assert len(chunks) > 1
    assert all(isinstance(c, str) for c in chunks)


def test_chunk_text_empty():
    assert chunk_text("") == []


def test_chunk_overlap():
    words = [f"w{i}" for i in range(30)]
    text = " ".join(words)
    chunks = chunk_text(text, chunk_size=10, overlap=3)
    # Second chunk should start before word 10 due to overlap
    assert len(chunks) >= 2


def test_strip_markdown():
    md = "# Heading\n**bold** and *italic* and `code`"
    plain = strip_markdown(md)
    assert "#" not in plain
    assert "**" not in plain
    assert "Heading" in plain
    assert "bold" in plain


@pytest.mark.asyncio
async def test_ingest_file(db):
    import uuid
    from app.models.workspace import Workspace

    ws = Workspace(name="test-ws")
    db.add(ws)
    await db.commit()
    await db.refresh(ws)

    content = b"# Incident\nService: payment-api\nSeverity: high\nRoot cause: db pool exhaustion\nFix: increase pool size"
    doc = await ingest_file(db, ws.id, "test-incident.md", content)
    assert doc.id is not None
    assert doc.filename == "test-incident.md"
    assert doc.doc_type in ("incident", "document", "runbook", "postmortem", "log")

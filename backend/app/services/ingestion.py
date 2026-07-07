from __future__ import annotations

import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.document import Document
from app.models.chunk import Chunk
from app.models.entity import Entity
from app.models.relationship import Relationship
from app.services.embedding import embed_texts
from app.services.entity_extraction import extract_entities
from app.utils.text_processing import parse_file_content, detect_doc_type, chunk_text, strip_markdown
from app.config import settings


async def ingest_file(
    db: AsyncSession,
    workspace_id: uuid.UUID,
    filename: str,
    raw_bytes: bytes,
) -> Document:
    """Full ingestion pipeline: parse → chunk → embed → extract entities → store."""
    content = parse_file_content(filename, raw_bytes)
    clean_content = strip_markdown(content)
    doc_type = detect_doc_type(filename, clean_content)

    doc = Document(
        workspace_id=workspace_id,
        filename=filename,
        doc_type=doc_type,
        content=clean_content,
        metadata_={"original_filename": filename},
    )
    db.add(doc)
    await db.flush()  # get doc.id without committing

    # Chunk
    chunks_text = chunk_text(clean_content, settings.chunk_size, settings.chunk_overlap)

    # Embed all chunks in one batch
    if chunks_text:
        vectors = embed_texts(chunks_text, settings.embedding_model)
    else:
        vectors = []

    chunk_objects = []
    for idx, (text, vec) in enumerate(zip(chunks_text, vectors)):
        c = Chunk(
            document_id=doc.id,
            workspace_id=workspace_id,
            content=text,
            chunk_index=idx,
            embedding=vec,
        )
        db.add(c)
        chunk_objects.append(c)

    # Entity extraction
    raw_entities = extract_entities(clean_content, filename)
    entity = Entity(
        document_id=doc.id,
        workspace_id=workspace_id,
        service_name=raw_entities.get("service_name"),
        error_type=raw_entities.get("error_type"),
        severity=raw_entities.get("severity"),
        root_cause=raw_entities.get("root_cause"),
        fix_or_workaround=raw_entities.get("fix_or_workaround"),
        related_runbook=raw_entities.get("related_runbook"),
        incident_date=raw_entities.get("incident_date"),
        raw_metadata=raw_entities,
    )
    db.add(entity)
    await db.flush()

    # Store knowledge-graph relationships
    await _store_relationships(db, workspace_id, doc, entity)

    await db.commit()
    await db.refresh(doc)
    return doc


async def _store_relationships(
    db: AsyncSession,
    workspace_id: uuid.UUID,
    doc: Document,
    entity: Entity,
) -> None:
    def add_rel(target_id: uuid.UUID, target_type: str, rel_type: str):
        db.add(
            Relationship(
                workspace_id=workspace_id,
                source_id=doc.id,
                source_type="document",
                target_id=target_id,
                target_type=target_type,
                relationship_type=rel_type,
            )
        )

    add_rel(entity.id, "entity", "has_entity")

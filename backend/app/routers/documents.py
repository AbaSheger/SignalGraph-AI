import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.workspace import Workspace
from app.models.document import Document
from app.models.entity import Entity
from app.models.chunk import Chunk
from app.schemas.document import DocumentRead
from app.services.ingestion import ingest_file

router = APIRouter(prefix="/workspaces", tags=["documents"])

_ALLOWED_EXTENSIONS = {"md", "txt", "json"}


def _check_workspace(ws: Workspace | None) -> None:
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")


@router.post("/{workspace_id}/upload", response_model=DocumentRead, status_code=201)
async def upload_file(
    workspace_id: uuid.UUID,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    ws = await db.get(Workspace, workspace_id)
    _check_workspace(ws)

    ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    if ext not in _ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=422,
            detail=f"Unsupported file type '.{ext}'. Allowed: {_ALLOWED_EXTENSIONS}",
        )
    raw = await file.read()
    doc = await ingest_file(db, workspace_id, file.filename or "upload", raw)
    return doc


@router.get("/{workspace_id}/sources", response_model=list[DocumentRead])
async def list_sources(workspace_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    ws = await db.get(Workspace, workspace_id)
    _check_workspace(ws)
    result = await db.execute(
        select(Document)
        .where(Document.workspace_id == workspace_id)
        .order_by(Document.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{workspace_id}/incidents")
async def list_incidents(workspace_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    ws = await db.get(Workspace, workspace_id)
    _check_workspace(ws)
    stmt = (
        select(Document, Entity)
        .outerjoin(Entity, Entity.document_id == Document.id)
        .where(Document.workspace_id == workspace_id)
        .where(Document.doc_type == "incident")
    )
    rows = (await db.execute(stmt)).all()
    return [
        {
            "id": str(doc.id),
            "filename": doc.filename,
            "doc_type": doc.doc_type,
            "service_name": ent.service_name if ent else None,
            "error_type": ent.error_type if ent else None,
            "severity": ent.severity if ent else None,
            "root_cause": ent.root_cause if ent else None,
            "fix_or_workaround": ent.fix_or_workaround if ent else None,
            "related_runbook": ent.related_runbook if ent else None,
            "incident_date": str(ent.incident_date) if ent and ent.incident_date else None,
        }
        for doc, ent in rows
    ]


@router.get("/{workspace_id}/runbooks")
async def list_runbooks(workspace_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    ws = await db.get(Workspace, workspace_id)
    _check_workspace(ws)
    result = await db.execute(
        select(Document)
        .where(Document.workspace_id == workspace_id)
        .where(Document.doc_type == "runbook")
    )
    docs = result.scalars().all()
    return [{"id": str(d.id), "filename": d.filename, "created_at": str(d.created_at)} for d in docs]


@router.get("/{workspace_id}/services")
async def list_services(workspace_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    ws = await db.get(Workspace, workspace_id)
    _check_workspace(ws)
    result = await db.execute(
        select(Entity.service_name)
        .where(Entity.workspace_id == workspace_id)
        .where(Entity.service_name.isnot(None))
        .distinct()
    )
    services = result.scalars().all()
    return {"services": services}

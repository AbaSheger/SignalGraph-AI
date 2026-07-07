import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.workspace import Workspace
from app.services.pattern_detection import detect_patterns

router = APIRouter(prefix="/workspaces", tags=["dashboard"])


@router.get("/{workspace_id}/patterns")
async def get_patterns(workspace_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    ws = await db.get(Workspace, workspace_id)
    if not ws:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return await detect_patterns(db, workspace_id)

import uuid
from datetime import datetime
from pydantic import BaseModel


class DocumentRead(BaseModel):
    id: uuid.UUID
    workspace_id: uuid.UUID
    filename: str
    doc_type: str
    created_at: datetime

    model_config = {"from_attributes": True}

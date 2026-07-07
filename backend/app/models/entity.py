import uuid
from datetime import date
from sqlalchemy import Text, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Entity(Base):
    __tablename__ = "entities"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    service_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    severity: Mapped[str | None] = mapped_column(Text, nullable=True)
    root_cause: Mapped[str | None] = mapped_column(Text, nullable=True)
    fix_or_workaround: Mapped[str | None] = mapped_column(Text, nullable=True)
    related_runbook: Mapped[str | None] = mapped_column(Text, nullable=True)
    incident_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    raw_metadata: Mapped[dict] = mapped_column(JSON, default=dict)

    document = relationship("Document", back_populates="entities")
    workspace = relationship("Workspace", back_populates="entities")

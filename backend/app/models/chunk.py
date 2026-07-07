import uuid
from sqlalchemy import Text, Integer, ForeignKey, JSON, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    document_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("documents.id", ondelete="CASCADE"))
    workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    # Store embedding as JSON list for SQLite compatibility; pgvector handled at query time
    embedding = Column(JSON, nullable=True)
    metadata_: Mapped[dict] = mapped_column("metadata", JSON, default=dict)

    document = relationship("Document", back_populates="chunks")
    workspace = relationship("Workspace", back_populates="chunks")

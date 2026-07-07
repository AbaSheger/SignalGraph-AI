from pydantic import BaseModel


class Citation(BaseModel):
    source: str
    chunk_index: int
    score: float
    excerpt: str


class QueryRequest(BaseModel):
    query: str
    filters: dict | None = None


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    citations: list[Citation]
    missing_evidence: list[str]

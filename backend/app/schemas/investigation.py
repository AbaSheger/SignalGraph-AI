from pydantic import BaseModel
from app.schemas.query import Citation


class InvestigationRequest(BaseModel):
    query: str


class InvestigationStep(BaseModel):
    step: int
    name: str
    result: str


class SimilarIncident(BaseModel):
    document_id: str
    filename: str
    score: float
    service_name: str | None
    root_cause: str | None
    fix_or_workaround: str | None
    related_runbook: str | None
    excerpt: str


class InvestigationResponse(BaseModel):
    query_type: str
    steps: list[InvestigationStep]
    similar_incidents: list[SimilarIncident]
    relevant_runbooks: list[str]
    answer: str
    confidence: float
    citations: list[Citation]
    missing_evidence: list[str]

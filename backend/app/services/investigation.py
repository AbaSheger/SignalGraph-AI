from __future__ import annotations

import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.retrieval import retrieve_chunks
from app.services.similarity import find_similar_incidents
from app.services.embedding import embed_texts, cosine_similarity
from app.services.llm import MockLlmService
from app.schemas.investigation import InvestigationResponse, InvestigationStep, SimilarIncident
from app.schemas.query import Citation
from app.config import settings


_QUERY_TYPES = {
    "incident": ["error", "exception", "timeout", "down", "failure", "crash", "outage"],
    "log": ["at line", "traceback", "stack trace", "stderr", "stdout", "pid", "exit code"],
    "question": ["what", "how", "why", "when", "which", "who"],
}


def classify_query(query: str) -> str:
    lower = query.lower()
    for qtype, keywords in _QUERY_TYPES.items():
        if any(kw in lower for kw in keywords):
            return qtype
    return "question"


async def run_investigation(
    db: AsyncSession,
    workspace_id: uuid.UUID,
    query: str,
) -> InvestigationResponse:
    steps: list[InvestigationStep] = []

    # Step 1 — Classify
    query_type = classify_query(query)
    steps.append(InvestigationStep(step=1, name="classify", result=f"Query classified as: {query_type}"))

    # Step 2 — Search similar incidents
    similar_raw = await find_similar_incidents(db, workspace_id, query)
    steps.append(
        InvestigationStep(
            step=2,
            name="search_incidents",
            result=f"Found {len(similar_raw)} similar incident(s).",
        )
    )

    # Step 3 — Search relevant runbooks
    runbook_chunks = await retrieve_chunks(db, workspace_id, query + " runbook procedure")
    runbook_names = list({
        c["filename"] for c in runbook_chunks
        if "runbook" in c["filename"].lower()
    })
    steps.append(
        InvestigationStep(
            step=3,
            name="search_runbooks",
            result=f"Found {len(runbook_names)} relevant runbook(s): {', '.join(runbook_names) or 'none'}",
        )
    )

    # Step 4 — Collect evidence / citations
    chunks = await retrieve_chunks(db, workspace_id, query, k=settings.max_chunks_retrieved)
    query_vec = embed_texts([query])[0]
    citations: list[Citation] = []
    for c in chunks:
        score = cosine_similarity(query_vec, []) if not c.get("embedding") else 0.0
        citations.append(Citation(
            source=c["filename"],
            chunk_index=c["chunk_index"],
            score=round(c.get("score", 0.0), 4),
            excerpt=c["content"][:200],
        ))
    steps.append(
        InvestigationStep(
            step=4,
            name="collect_evidence",
            result=f"Collected {len(citations)} evidence chunk(s).",
        )
    )

    # Step 5 — Generate answer
    llm = MockLlmService()
    llm_result = llm.generate_answer(query, chunks, [c.model_dump() for c in citations])
    steps.append(
        InvestigationStep(
            step=5,
            name="generate_answer",
            result="Answer generated with citations.",
        )
    )

    similar_incidents = [
        SimilarIncident(
            document_id=s["document_id"],
            filename=s["filename"],
            score=s["score"],
            service_name=s.get("service_name"),
            root_cause=s.get("root_cause"),
            fix_or_workaround=s.get("fix_or_workaround"),
            related_runbook=s.get("related_runbook"),
            excerpt=s.get("excerpt", ""),
        )
        for s in similar_raw
    ]

    return InvestigationResponse(
        query_type=query_type,
        steps=steps,
        similar_incidents=similar_incidents,
        relevant_runbooks=runbook_names,
        answer=llm_result["answer"],
        confidence=llm_result["confidence"],
        citations=citations,
        missing_evidence=llm_result["missing_evidence"],
    )

from __future__ import annotations

import uuid
from collections import Counter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entity import Entity
from app.models.document import Document


async def detect_patterns(db: AsyncSession, workspace_id: uuid.UUID) -> dict:
    """Analyse entities to find repeated incidents, error types and missing data."""
    stmt = (
        select(Entity)
        .where(Entity.workspace_id == workspace_id)
    )
    entities = (await db.execute(stmt)).scalars().all()

    service_counter: Counter = Counter()
    error_counter: Counter = Counter()
    fix_counter: Counter = Counter()
    no_root_cause: list[str] = []
    no_runbook_services: list[str] = []

    doc_ids_no_root_cause: list[uuid.UUID] = []

    for e in entities:
        if e.service_name:
            service_counter[e.service_name] += 1
        if e.error_type:
            error_counter[e.error_type] += 1
        if e.fix_or_workaround:
            fix_counter[e.fix_or_workaround[:80]] += 1
        if not e.root_cause:
            doc_ids_no_root_cause.append(e.document_id)
        if e.service_name and not e.related_runbook:
            no_runbook_services.append(e.service_name)

    # Fetch filenames for docs without root cause
    docs_stmt = select(Document.filename).where(
        Document.id.in_(doc_ids_no_root_cause)
    )
    missing_rootcause_docs = list(
        (await db.execute(docs_stmt)).scalars().all()
    )

    return {
        "top_services": service_counter.most_common(10),
        "recurring_errors": [e for e, c in error_counter.most_common(10) if c > 0],
        "reusable_fixes": [f for f, c in fix_counter.most_common(5) if c >= 1],
        "incidents_without_root_cause": missing_rootcause_docs,
        "services_missing_runbook": list(set(no_runbook_services)),
    }

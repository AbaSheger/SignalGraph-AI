import pytest
from app.services.entity_extraction import extract_entities


INCIDENT_TEXT = """
# Payment API Timeout Incident
Date: 2024-03-15
Service: payment-api
Severity: high
Error: ConnectionTimeout

Root cause: upstream database connection pool exhaustion
Fix: increase pool size and add circuit breaker
Runbook: deployment-rollback-runbook.md
"""

POSTMORTEM_TEXT = """
# Auth Service Postmortem
Incident Date: 2024-04-01
Affected service: auth-service
Error: JWTValidationError
Severity: critical

Root cause: expired signing key
Fix: rotate signing key
"""


def test_extract_service_name():
    entities = extract_entities(INCIDENT_TEXT, "payment-api-timeout.md")
    assert entities["service_name"] == "payment-api"


def test_extract_error_type():
    entities = extract_entities(INCIDENT_TEXT)
    assert entities["error_type"] is not None
    assert "Timeout" in entities["error_type"] or "Connection" in entities["error_type"]


def test_extract_severity():
    entities = extract_entities(INCIDENT_TEXT)
    assert entities["severity"] == "high"


def test_extract_root_cause():
    entities = extract_entities(INCIDENT_TEXT)
    assert entities["root_cause"] is not None
    assert "pool" in entities["root_cause"].lower() or "database" in entities["root_cause"].lower()


def test_extract_fix():
    entities = extract_entities(INCIDENT_TEXT)
    assert entities["fix_or_workaround"] is not None
    assert "pool" in entities["fix_or_workaround"].lower() or "circuit" in entities["fix_or_workaround"].lower()


def test_extract_runbook():
    entities = extract_entities(INCIDENT_TEXT, "payment-api-timeout.md")
    assert entities["related_runbook"] == "deployment-rollback-runbook.md"


def test_extract_date():
    entities = extract_entities(INCIDENT_TEXT)
    assert entities["incident_date"] is not None


def test_extract_critical_severity():
    entities = extract_entities(POSTMORTEM_TEXT)
    assert entities["severity"] == "critical"


def test_extract_jwt_error():
    entities = extract_entities(POSTMORTEM_TEXT)
    assert entities["error_type"] is not None
    assert "JWT" in entities["error_type"] or "Validation" in entities["error_type"]


def test_empty_text():
    entities = extract_entities("")
    assert entities["service_name"] is None
    assert entities["error_type"] is None

import re
from datetime import date


_SERVICE_PATTERNS = [
    r"service[:\s]+([a-z][a-z0-9\-_]+)",
    r"affected service[:\s]+([a-z][a-z0-9\-_]+)",
]
_ERROR_PATTERNS = [
    r"error[:\s]+([A-Z][A-Za-z0-9]+(?:Error|Exception|Timeout|Lag|Failure))",
    r"exception[:\s]+([A-Z][A-Za-z0-9]+(?:Error|Exception|Timeout|Lag|Failure))",
    r"([A-Z][A-Za-z0-9]+(?:Error|Exception|Timeout|Lag|Failure))",
]
_SEVERITY_VALUES = {"critical", "high", "medium", "low", "sev-1", "sev-2", "sev-3", "sev-4"}
_SEVERITY_PATTERN = r"severity[:\s]+(critical|high|medium|low|sev-[1-4])"
_ROOT_CAUSE_PATTERN = r"root cause[:\s]+(.+?)(?:\n|$)"
_FIX_PATTERN = r"(?:fix|resolution|workaround)[:\s]+(.+?)(?:\n|$)"
_RUNBOOK_PATTERN = r"runbook[:\s]+([^\n]+\.md)"
_DATE_PATTERN = r"(\d{4}-\d{2}-\d{2})"


def extract_entities(text: str, filename: str = "") -> dict:
    """Run rule-based extraction and return a flat entity dict."""
    lower = text.lower()
    return {
        "service_name": _first_match(_SERVICE_PATTERNS, lower),
        "error_type": _first_match(_ERROR_PATTERNS, text),
        "severity": _extract_severity(lower),
        "root_cause": _first_match_str([_ROOT_CAUSE_PATTERN], text),
        "fix_or_workaround": _first_match_str([_FIX_PATTERN], text),
        "related_runbook": _extract_runbook(text, filename),
        "incident_date": _extract_date(text),
    }


def _first_match(patterns: list[str], text: str) -> str | None:
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def _first_match_str(patterns: list[str], text: str) -> str | None:
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            value = m.group(1).strip()
            return value[:200] if value else None
    return None


def _extract_severity(text: str) -> str | None:
    m = re.search(_SEVERITY_PATTERN, text, re.IGNORECASE)
    if m:
        return m.group(1).lower()
    for sev in _SEVERITY_VALUES:
        if sev in text:
            return sev
    return None


def _extract_runbook(text: str, filename: str) -> str | None:
    m = re.search(_RUNBOOK_PATTERN, text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    if "runbook" in filename.lower():
        return filename
    return None


def _extract_date(text: str) -> date | None:
    m = re.search(_DATE_PATTERN, text)
    if m:
        try:
            return date.fromisoformat(m.group(1))
        except ValueError:
            return None
    return None

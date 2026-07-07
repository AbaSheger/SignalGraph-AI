import re
import json
from typing import Iterator


def parse_file_content(filename: str, raw_bytes: bytes) -> str:
    """Return the plain text content of a file regardless of format."""
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext == "json":
        try:
            data = json.loads(raw_bytes.decode("utf-8", errors="replace"))
            return json.dumps(data, indent=2)
        except json.JSONDecodeError:
            pass
    return raw_bytes.decode("utf-8", errors="replace")


def detect_doc_type(filename: str, content: str) -> str:
    """Heuristically classify a document based on name and content."""
    name_lower = filename.lower()
    content_lower = content.lower()
    if "runbook" in name_lower:
        return "runbook"
    if "postmortem" in name_lower:
        return "postmortem"
    if any(kw in content_lower for kw in ("postmortem", "post-mortem", "post mortem")):
        return "postmortem"
    if any(kw in content_lower for kw in ("runbook", "procedure", "playbook")):
        return "runbook"
    if any(kw in content_lower for kw in ("incident", "severity", "root cause", "sev-")):
        return "incident"
    if any(kw in content_lower for kw in ("log ", "error:", "exception", "stack trace")):
        return "log"
    return "document"


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 64) -> list[str]:
    """Split text into overlapping chunks on word boundaries."""
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        if end >= len(words):
            break
        start += chunk_size - overlap
    return chunks


def strip_markdown(text: str) -> str:
    """Remove common Markdown syntax, leaving plain text."""
    text = re.sub(r"#{1,6}\s+", "", text)
    text = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", text)
    text = re.sub(r"_{1,2}(.+?)_{1,2}", r"\1", text)
    text = re.sub(r"`{1,3}[^`]*`{1,3}", "", text, flags=re.DOTALL)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[(.+?)\]\(.*?\)", r"\1", text)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

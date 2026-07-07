from app.services.llm.base import LlmService


class MockLlmService(LlmService):
    """Deterministic mock that constructs answers from retrieved context — no API keys required."""

    def generate_answer(
        self,
        query: str,
        context_chunks: list[dict],
        citations: list[dict],
    ) -> dict:
        answer = self._build_answer(query, context_chunks)
        confidence = min(1.0, len(context_chunks) * 0.2)
        missing_evidence = self._detect_missing_evidence(context_chunks)
        return {
            "answer": answer,
            "confidence": round(confidence, 2),
            "missing_evidence": missing_evidence,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_answer(self, query: str, chunks: list[dict]) -> str:
        if not chunks:
            return (
                f"No relevant documents were found for: '{query}'. "
                "Please ingest incident reports or runbooks before querying."
            )
        sources = list({c.get("filename", "unknown") for c in chunks})
        source_str = ", ".join(f"'{s}'" for s in sources)
        excerpts = []
        for c in chunks[:3]:
            text = c.get("content", "")[:200].strip()
            if text:
                excerpts.append(f"- {text}…")
        excerpt_block = "\n".join(excerpts)
        return (
            f"Based on the ingested documents ({source_str}), here is what was found "
            f"for the query '{query}':\n\n{excerpt_block}\n\n"
            "Review the cited sources below for full context."
        )

    def _detect_missing_evidence(self, chunks: list[dict]) -> list[str]:
        missing = []
        texts = " ".join(c.get("content", "") for c in chunks).lower()
        if not any(kw in texts for kw in ("root cause", "cause", "reason")):
            missing.append("No root cause documented in retrieved context.")
        if not any(kw in texts for kw in ("fix", "resolution", "workaround", "resolve")):
            missing.append("No fix or resolution documented in retrieved context.")
        return missing

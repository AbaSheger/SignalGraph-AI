from abc import ABC, abstractmethod


class LlmService(ABC):
    @abstractmethod
    def generate_answer(
        self,
        query: str,
        context_chunks: list[dict],
        citations: list[dict],
    ) -> dict:
        """Return {"answer": str, "confidence": float, "missing_evidence": list[str]}."""

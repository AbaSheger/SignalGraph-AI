from app.services.llm.base import LlmService
from app.services.llm.mock import MockLlmService


def get_llm_service(provider: str = "mock") -> LlmService:
    if provider == "mock":
        return MockLlmService()
    raise ValueError(f"Unknown LLM provider: {provider}")

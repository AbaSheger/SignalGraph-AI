from __future__ import annotations

import hashlib

import numpy as np

# None = not yet attempted; False = failed to load; model instance = loaded
_model = None


def _get_model(model_name: str):
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _model = SentenceTransformer(model_name)
        except Exception:
            _model = False  # sentinel: loading failed, do not retry
    return _model if _model is not False else None


def _hash_embed(text: str, dim: int = 384) -> list[float]:
    """Deterministic embedding from text hash — used as offline fallback."""
    seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16) % (2**31)
    rng = np.random.default_rng(seed)
    vec = rng.standard_normal(dim).astype(float)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()


def embed_texts(texts: list[str], model_name: str = "all-MiniLM-L6-v2") -> list[list[float]]:
    """Return normalised embedding vectors. Falls back to hash embeddings when model unavailable."""
    if not texts:
        return []
    model = _get_model(model_name)
    if model is None:
        return [_hash_embed(t) for t in texts]
    try:
        vectors = model.encode(texts, normalize_embeddings=True)
        return [v.tolist() for v in vectors]
    except Exception:
        return [_hash_embed(t) for t in texts]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)

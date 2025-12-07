"""Synthetic embedding utilities using deterministic hashing for reproducibility."""

from __future__ import annotations

import hashlib
from typing import List

import numpy as np


def _hash_to_vector(text: str, dim: int = 64) -> np.ndarray:
    """Convert text to pseudo-random vector using hashing for reproducibility."""

    digest = hashlib.sha256(text.encode("utf-8")).digest()
    repeat_times = (dim // len(digest)) + 1
    raw_bytes = (digest * repeat_times)[:dim]
    vector = np.frombuffer(raw_bytes, dtype=np.uint8).astype(np.float32)
    norm = np.linalg.norm(vector)
    if norm == 0:
        return np.zeros(dim, dtype=np.float32)
    normalized = vector / norm
    return normalized


def embed_text(sentences: List[str], dim: int = 64) -> np.ndarray:
    """Generate synthetic embeddings for a list of sentences."""

    if not sentences:
        raise ValueError("sentences must contain at least one item to embed")
    normalized_sentences = [str(sentence) for sentence in sentences]
    return np.vstack([_hash_to_vector(sentence, dim) for sentence in normalized_sentences])


def similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """Compute cosine similarity matrix for embeddings."""

    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1e-8, norms)
    normed = embeddings / norms
    return np.clip(normed @ normed.T, -1.0, 1.0)

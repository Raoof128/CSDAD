"""Unit tests for embedding utilities to guarantee stability."""

from __future__ import annotations

import numpy as np
import pytest

from backend.utils.embeddings import embed_text, similarity_matrix


def test_embed_text_handles_empty_input():
    """Embedding generator should not raise when a string is empty."""

    vectors = embed_text([""])
    assert vectors.shape == (1, 64)
    assert np.isfinite(vectors).all()


def test_embed_text_rejects_empty_list():
    """Embedding generator should reject empty input collections."""

    with pytest.raises(ValueError):
        embed_text([])


def test_similarity_matrix_no_nan_for_zero_vectors():
    """Similarity computation should guard against zero division."""

    zero_vectors = np.zeros((2, 64), dtype=np.float32)
    matrix = similarity_matrix(zero_vectors)
    assert matrix.shape == (2, 2)
    assert np.isfinite(matrix).all()

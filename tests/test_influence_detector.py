"""Tests for influence detector validation and clustering safeguards."""

from __future__ import annotations

import numpy as np
import pytest

from backend.engines.influence_detector import InfluenceDetector


def test_influence_rejects_empty_embeddings():
    detector = InfluenceDetector()
    with pytest.raises(ValueError):
        detector.analyze(np.array([]))


def test_influence_rejects_nonfinite_embeddings():
    detector = InfluenceDetector()
    bad_vectors = np.array([[np.nan, 0.1], [0.2, 0.3]])
    with pytest.raises(ValueError):
        detector.analyze(bad_vectors)


def test_influence_handles_single_embedding():
    detector = InfluenceDetector()
    single = np.array([[0.1, 0.2]])
    result = detector.analyze(single)
    assert result.score == 5.0
    assert "cluster_0" in result.narrative_clusters

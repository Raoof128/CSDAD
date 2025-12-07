"""Simulated coordinated influence detection using clustering heuristics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from sklearn.cluster import KMeans

from ..utils.embeddings import similarity_matrix
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class InfluenceSignals:
    score: float
    narrative_clusters: Dict[str, List[int]]
    similarity_heatmap_path: str

    def to_dict(self) -> Dict[str, object]:
        """Serialize influence results for downstream use."""

        return {
            "score": self.score,
            "narrative_clusters": self.narrative_clusters,
            "similarity_heatmap_path": self.similarity_heatmap_path,
        }


class InfluenceDetector:
    """Cluster embeddings to simulate narrative grouping."""

    def analyze(self, embeddings: np.ndarray) -> InfluenceSignals:
        """Cluster embedding vectors and derive a coordination score."""

        embeddings = np.asarray(embeddings, dtype=float)
        if embeddings.size == 0:
            raise ValueError("Embeddings array is empty; cannot analyze influence patterns")
        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D array of shape (n_items, n_dims)")
        if embeddings.shape[1] == 0:
            raise ValueError("Embeddings must contain at least one dimension")
        if not np.all(np.isfinite(embeddings)):
            raise ValueError("Embeddings contain non-finite values and cannot be clustered")

        if embeddings.shape[0] < 2:
            return InfluenceSignals(
                score=5.0, narrative_clusters={"cluster_0": [0]}, similarity_heatmap_path=""
            )

        matrix = similarity_matrix(embeddings)
        n_clusters = min(3, embeddings.shape[0])
        kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42)
        labels = kmeans.fit_predict(embeddings)
        clusters: Dict[str, List[int]] = {}
        for idx, label in enumerate(labels):
            clusters.setdefault(f"cluster_{label}", []).append(idx)

        max_similarity = float(np.max(matrix))
        score = round(max_similarity * 100, 2)

        from ..utils.visuals import save_heatmap  # imported lazily to avoid circular deps

        heatmap_path = save_heatmap(
            matrix, [f"c{i}" for i in range(embeddings.shape[0])], "similarity"
        )
        logger.info("Influence detection score=%s clusters=%s", score, clusters)
        return InfluenceSignals(
            score=score, narrative_clusters=clusters, similarity_heatmap_path=heatmap_path
        )

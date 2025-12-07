"""Synthetic misinformation detector built on heuristic patterns."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class MisinfoSignals:
    score: float
    flagged_sentences: List[str]
    explanation: str

    def to_dict(self) -> dict[str, object]:
        """Serialize misinformation findings for API responses."""

        return {
            "score": self.score,
            "flagged_sentences": self.flagged_sentences,
            "explanation": self.explanation,
        }


class MisinfoDetector:
    """Flag fabricated statistics, exaggerated claims, and unsupported causal links."""

    def __init__(self) -> None:
        self.stats_patterns = ["%", "percent", "study shows", "experts agree"]
        self.exaggeration_markers = ["guaranteed", "never fails", "perfect", "always"]
        self.causal_markers = ["therefore", "so", "which means", "as a result"]

    def analyze(self, text: str) -> MisinfoSignals:
        """Heuristically score text for synthetic misinformation patterns."""

        sentences = [sent.strip() for sent in text.split(".") if sent.strip()]
        flagged: List[str] = []
        signal_strength = 0

        for sentence in sentences:
            lower = sentence.lower()
            hits = sum(marker in lower for marker in self.stats_patterns)
            hits += sum(marker in lower for marker in self.exaggeration_markers)
            hits += sum(marker in lower for marker in self.causal_markers)
            if hits >= 2:
                flagged.append(sentence)
            signal_strength += hits

        normalized_score = min(100.0, signal_strength * 5)
        explanation = (
            "Synthetic classifier looks for exaggerated certainty, repeated statistics, and causal chains "
            "without evidence."
        )

        logger.info("Misinfo analysis score=%s flagged=%s", normalized_score, len(flagged))
        return MisinfoSignals(
            score=normalized_score, flagged_sentences=flagged, explanation=explanation
        )

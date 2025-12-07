"""Fusion engine to compute cognitive risk scores."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class RiskResult:
    score: float
    level: str
    explanation: List[str]

    def to_dict(self) -> Dict[str, object]:
        """Serialize the computed risk into a dictionary."""

        return {"score": self.score, "level": self.level, "explanation": self.explanation}


class RiskEngine:
    """Combine multiple signals into a single cognitive risk score."""

    def classify(self, score: float) -> str:
        """Map a numeric score to a categorical level."""

        if score >= 85:
            return "CRITICAL"
        if score >= 65:
            return "HIGH"
        if score >= 40:
            return "MEDIUM"
        return "LOW"

    def compute(
        self,
        manipulation_score: float,
        misinfo_score: float,
        influence_score: float,
        domain_credibility: float,
        emotional_intensity: float,
        deception_markers: int,
    ) -> RiskResult:
        """Fuse scores from multiple detectors into a single risk result."""

        weighted = (
            manipulation_score * 0.25
            + misinfo_score * 0.25
            + influence_score * 0.2
            + emotional_intensity * 0.1
            + deception_markers * 5
            + (100 - domain_credibility) * 0.2
        )
        score = min(100.0, round(weighted, 2))
        level = self.classify(score)

        explanation = [
            f"Manipulation score contribution: {manipulation_score:.1f}",
            f"Misinformation score contribution: {misinfo_score:.1f}",
            f"Influence coordination contribution: {influence_score:.1f}",
            f"Domain credibility penalty: {(100 - domain_credibility) * 0.2:.1f}",
            f"Emotional intensity contribution: {emotional_intensity:.1f}",
            f"Deception markers contribution: {deception_markers * 5:.1f}",
        ]

        logger.info("Risk computed score=%s level=%s", score, level)
        return RiskResult(score=score, level=level, explanation=explanation)

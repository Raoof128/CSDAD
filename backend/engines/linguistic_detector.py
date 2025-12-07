"""Linguistic manipulation detector leveraging spaCy cues and keyword heuristics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import spacy
from spacy.lang.en import English

from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class LinguisticSignals:
    manipulation_score: float
    emotional_intensity: float
    flags: List[str]

    def to_dict(self) -> Dict[str, object]:
        """Serialize signals to a dictionary for API responses."""

        return {
            "manipulation_score": self.manipulation_score,
            "emotional_intensity": self.emotional_intensity,
            "flags": self.flags,
        }


class LinguisticDetector:
    """Detects emotional and manipulation signals using lightweight heuristics."""

    def __init__(self) -> None:
        try:
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy model en_core_web_sm")
        except Exception:  # pragma: no cover - fallback when model unavailable
            logger.warning("spaCy model unavailable; using blank pipeline")
            self.nlp = English()
            if not self.nlp.has_pipe("sentencizer"):
                self.nlp.add_pipe("sentencizer")

        self.fear_words = {"urgent", "panic", "immediately", "threat", "crisis"}
        self.anger_words = {"furious", "outrage", "exploit", "abuse"}
        self.certainty_modals = {"always", "never", "undeniably", "guaranteed"}
        self.hedging = {"maybe", "might", "could", "possible"}

    def analyze(self, text: str) -> LinguisticSignals:
        """Score linguistic manipulation and emotional cues in text."""

        doc = self.nlp(text)
        tokens = [token.text.lower() for token in doc]

        fear_hits = sum(token in self.fear_words for token in tokens)
        anger_hits = sum(token in self.anger_words for token in tokens)
        certainty_hits = sum(token in self.certainty_modals for token in tokens)
        hedge_hits = sum(token in self.hedging for token in tokens)

        emotional_intensity = min(1.0, (fear_hits + anger_hits) / max(len(tokens), 1))
        manipulation_score = min(1.0, (certainty_hits + fear_hits * 1.2) / max(len(tokens), 1))

        flags: List[str] = []
        if fear_hits:
            flags.append("fear appeals detected")
        if anger_hits:
            flags.append("anger language present")
        if certainty_hits:
            flags.append("overconfidence markers")
        if hedge_hits:
            flags.append("hedging statements found")

        logger.info(
            "Linguistic analysis complete: fear=%s, anger=%s, certainty=%s, hedge=%s",
            fear_hits,
            anger_hits,
            certainty_hits,
            hedge_hits,
        )

        return LinguisticSignals(
            manipulation_score=round(manipulation_score * 100, 2),
            emotional_intensity=round(emotional_intensity * 100, 2),
            flags=flags or ["neutral tone"],
        )

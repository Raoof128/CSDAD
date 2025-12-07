"""Cross-modal risk scoring endpoint."""

from __future__ import annotations

from typing import Any, Dict

import numpy as np
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..engines.influence_detector import InfluenceDetector
from ..engines.linguistic_detector import LinguisticDetector
from ..engines.misinfo_detector import MisinfoDetector
from ..engines.risk_engine import RiskEngine
from ..engines.text_analyzer import TextAnalyzer
from ..utils.logger import get_logger

router = APIRouter(prefix="/risk_score", tags=["risk"])
logger = get_logger(__name__)
text_analyzer = TextAnalyzer()
linguistic_detector = LinguisticDetector()
misinfo_detector = MisinfoDetector()
influence_detector = InfluenceDetector()
risk_engine = RiskEngine()


class RiskPayload(BaseModel):
    text_items: list[str] = Field(..., min_length=1, description="Collection of posts to fuse")
    domain_credibility: float = Field(80, ge=0, le=100)


@router.post("")
def compute_risk(payload: RiskPayload) -> Dict[str, Any]:
    """Compute a fused cognitive risk score across multiple synthetic posts."""

    try:
        analyses = [text_analyzer.analyze_text(item) for item in payload.text_items]
        embeddings = [a.vector for a in analyses]
        linguistic = [linguistic_detector.analyze(a.clean_text) for a in analyses]
        misinfo = [misinfo_detector.analyze(a.clean_text) for a in analyses]
        influence = influence_detector.analyze(np.array(embeddings))
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Risk computation failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    avg_manipulation = sum(signal.manipulation_score for signal in linguistic) / len(linguistic)
    avg_emotion = sum(signal.emotional_intensity for signal in linguistic) / len(linguistic)
    deception_markers = sum(
        "overconfidence" in flag for signal in linguistic for flag in signal.flags
    )
    avg_misinfo = sum(misinfo_signal.score for misinfo_signal in misinfo) / len(misinfo)

    risk = risk_engine.compute(
        manipulation_score=avg_manipulation,
        misinfo_score=avg_misinfo,
        influence_score=influence.score,
        domain_credibility=payload.domain_credibility,
        emotional_intensity=avg_emotion,
        deception_markers=deception_markers,
    )

    return {
        "risk": risk.to_dict(),
        "influence": influence.to_dict(),
        "linguistic": [signal.to_dict() for signal in linguistic],
        "misinformation": [misinfo_signal.to_dict() for misinfo_signal in misinfo],
    }

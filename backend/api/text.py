"""Text analysis endpoint."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from ..engines.linguistic_detector import LinguisticDetector
from ..engines.misinfo_detector import MisinfoDetector
from ..engines.text_analyzer import TextAnalyzer
from ..utils.logger import get_logger

router = APIRouter(prefix="/analyze_text", tags=["analysis"])
logger = get_logger(__name__)
text_analyzer = TextAnalyzer()
linguistic_detector = LinguisticDetector()
misinfo_detector = MisinfoDetector()


class TextPayload(BaseModel):
    text: str = Field(..., min_length=1, max_length=5_000)

    @field_validator("text")
    @classmethod
    def strip_and_validate(cls, value: str) -> str:
        """Ensure text is not blank after trimming whitespace."""

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("text cannot be empty or whitespace only")
        return cleaned


@router.post("")
def analyze_text(payload: TextPayload) -> Dict[str, Any]:
    """Analyze synthetic text and return embeddings plus heuristic signals."""

    try:
        analyzed = text_analyzer.analyze_text(payload.text)
        linguistic = linguistic_detector.analyze(analyzed.clean_text)
        misinfo = misinfo_detector.analyze(analyzed.clean_text)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Text analysis failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "clean_text": analyzed.clean_text,
        "vector_representation": analyzed.vector,
        "metadata": analyzed.metadata,
        "linguistic": linguistic.to_dict(),
        "misinformation": misinfo.to_dict(),
    }

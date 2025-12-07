"""URL analysis endpoint with synthetic fetch."""

from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, HttpUrl

from ..engines.linguistic_detector import LinguisticDetector
from ..engines.misinfo_detector import MisinfoDetector
from ..engines.text_analyzer import TextAnalyzer
from ..utils.logger import get_logger

router = APIRouter(prefix="/analyze_url", tags=["analysis"])
logger = get_logger(__name__)
text_analyzer = TextAnalyzer()
linguistic_detector = LinguisticDetector()
misinfo_detector = MisinfoDetector()


class UrlPayload(BaseModel):
    url: HttpUrl = Field(..., description="Synthetic URL to analyze")


@router.post("")
def analyze_url(payload: UrlPayload) -> Dict[str, Any]:
    """Analyze a synthetic URL by simulating content fetch and running detectors."""

    try:
        analyzed = text_analyzer.analyze_url(str(payload.url))
        linguistic = linguistic_detector.analyze(analyzed.clean_text)
        misinfo = misinfo_detector.analyze(analyzed.clean_text)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("URL analysis failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "clean_text": analyzed.clean_text,
        "vector_representation": analyzed.vector,
        "metadata": analyzed.metadata,
        "linguistic": linguistic.to_dict(),
        "misinformation": misinfo.to_dict(),
    }

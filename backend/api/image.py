"""Image analysis endpoint."""

from __future__ import annotations

import base64
from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator

from ..engines.linguistic_detector import LinguisticDetector
from ..engines.misinfo_detector import MisinfoDetector
from ..engines.text_analyzer import TextAnalyzer
from ..utils.logger import get_logger

router = APIRouter(prefix="/analyze_image", tags=["analysis"])
logger = get_logger(__name__)
text_analyzer = TextAnalyzer()
linguistic_detector = LinguisticDetector()
misinfo_detector = MisinfoDetector()


class ImagePayload(BaseModel):
    image_b64: str = Field(..., min_length=10, description="Base64-encoded synthetic image")

    @field_validator("image_b64")
    @classmethod
    def validate_base64(cls, value: str) -> str:
        """Ensure the provided string is valid base64 to prevent decode errors."""

        try:
            base64.b64decode(value, validate=True)
        except Exception as exc:  # pylint: disable=broad-except
            raise ValueError("image_b64 must be valid base64-encoded data") from exc
        return value


@router.post("")
def analyze_image(payload: ImagePayload) -> Dict[str, Any]:
    """Analyze a synthetic base64 image by running OCR and heuristic detectors."""

    try:
        analyzed = text_analyzer.analyze_image(payload.image_b64)
        linguistic = linguistic_detector.analyze(analyzed.clean_text)
        misinfo = misinfo_detector.analyze(analyzed.clean_text)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Image analysis failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return {
        "clean_text": analyzed.clean_text,
        "vector_representation": analyzed.vector,
        "metadata": analyzed.metadata,
        "linguistic": linguistic.to_dict(),
        "misinformation": misinfo.to_dict(),
    }

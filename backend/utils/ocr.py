"""Synthetic OCR helper for demo purposes."""

from __future__ import annotations

import base64
import io
from typing import Optional

from PIL import Image

from .logger import get_logger

logger = get_logger(__name__)


def extract_text_from_image(image_b64: str) -> Optional[str]:
    """Decode base64 image and return placeholder OCR text.

    In this synthetic environment we do not perform actual OCR; instead we
    demonstrate pipeline integration and log metadata.
    """

    try:
        image_bytes = base64.b64decode(image_b64)
        with Image.open(io.BytesIO(image_bytes)) as img:
            logger.info("Synthetic OCR processed image size %s", img.size)
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning("OCR decode failed: %s", exc)
        return None

    return "Synthetic OCR extracted text for demonstration purposes."

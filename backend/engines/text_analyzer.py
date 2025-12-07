"""Input analyzer for text, images, and URLs (synthetic)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict

from ..utils.embeddings import embed_text
from ..utils.logger import get_logger
from ..utils.ocr import extract_text_from_image

logger = get_logger(__name__)


@dataclass
class AnalyzedContent:
    """Container for standardized content payloads."""

    clean_text: str
    vector: list[float]
    metadata: Dict[str, str]


class TextAnalyzer:
    """Normalize inputs and produce synthetic embeddings."""

    def analyze_text(self, text: str) -> AnalyzedContent:
        """Clean free-form text and compute a deterministic embedding."""

        clean = text.strip()
        if not clean:
            logger.info("Received empty text payload after stripping whitespace")
            clean = "synthetic empty text"
        embedding = embed_text([clean])[0].tolist()
        metadata = {"source": "text", "length": str(len(clean))}
        logger.info("Analyzed text input length=%s", len(clean))
        return AnalyzedContent(clean_text=clean, vector=embedding, metadata=metadata)

    def analyze_image(self, image_b64: str) -> AnalyzedContent:
        """Decode a base64 image, run synthetic OCR, and embed the extracted text."""

        extracted = extract_text_from_image(image_b64) or ""
        clean = extracted.strip()
        payload = clean or "synthetic image"
        embedding = embed_text([payload])[0].tolist()
        metadata = {"source": "image", "ocr_available": str(bool(extracted))}
        logger.info("Analyzed image content; ocr_available=%s", bool(extracted))
        return AnalyzedContent(clean_text=clean, vector=embedding, metadata=metadata)

    def analyze_url(self, url: str) -> AnalyzedContent:
        """Simulate URL fetch to keep analysis fully offline and synthetic."""

        synthetic_payload = f"Synthetic fetch from {url} with fictional content."
        embedding = embed_text([synthetic_payload])[0].tolist()
        metadata = {"source": "url", "status": "simulated"}
        logger.info("Analyzed URL content for %s", url)
        return AnalyzedContent(clean_text=synthetic_payload, vector=embedding, metadata=metadata)

    def to_json(self, content: AnalyzedContent) -> str:
        """Serialize the analyzed content to JSON for logging or export."""

        return json.dumps(
            {
                "clean_text": content.clean_text,
                "vector": content.vector,
                "metadata": content.metadata,
            },
            indent=2,
        )

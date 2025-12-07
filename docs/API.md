# API Documentation

All endpoints operate on **synthetic content** only. Request and response bodies are validated with Pydantic models. Example responses omit some fields for brevity.

## POST /analyze_text
- **Body**: `{ "text": "fictional message" }` (trimmed; whitespace-only payloads are rejected)
- **Response**:
  ```json
  {
    "clean_text": "fictional message",
    "vector_representation": [0.1, ...],
    "metadata": {"source": "text", "length": "18"},
    "linguistic": {"manipulation_score": 12.5, "emotional_intensity": 7.5, "flags": []},
    "misinformation": {"score": 0.0, "flagged_sentences": [], "explanation": "..."}
  }
  ```

## POST /analyze_image
- **Body**: `{ "image_b64": "..." }` (must be valid base64)
- **Notes**: OCR is simulated; `clean_text` may be empty if decoding fails.

## POST /analyze_url
- **Body**: `{ "url": "https://example.invalid" }`
- **Notes**: Fetch is simulated; content is fabricated and processed offline.

## POST /risk_score
- **Body**: `{ "text_items": ["post one", "post two"], "domain_credibility": 75 }`
- **Response**:
  ```json
  {
    "risk": {"score": 48.5, "level": "MEDIUM", "explanation": ["..."]},
    "influence": {"score": 22.0, "narrative_clusters": {"cluster_0": [0,1]}, "similarity_heatmap_path": "reports/similarity.png"},
    "linguistic": [...],
    "misinformation": [...]
  }
  ```

## GET /dashboard
- **Response**: Ready message for the dashboard UI.

## GET /health
- **Response**: `{ "status": "ok" }`

### Error Handling
Errors return JSON with HTTP status codes and descriptive messages. Inputs are validated with Pydantic.

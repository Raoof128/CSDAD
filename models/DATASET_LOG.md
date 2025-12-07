# Synthetic Dataset Log

This project does **not** ship or process real-world data. All references, examples, and outputs are fabricated for educational demonstrations of cognitive security concepts.

## Sources
- Text inputs are provided ad-hoc by users and treated as fictional.
- Image analysis uses base64 payloads supplied at runtime; OCR is simulated and non-persistent.
- URL analysis is fully offline and generates synthetic placeholder content.

## Governance Notes
- No external calls are made to fetch live content.
- Logs are stored locally under `logs/` for observability only and can be rotated or deleted as needed.
- If additional synthetic corpora are added, document provenance and generation steps here to preserve reproducibility and safety.

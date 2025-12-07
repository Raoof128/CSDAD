# Contributing Guidelines

Thank you for considering a contribution to the Cognitive Security & Disinformation Analysis Dashboard. This project is **synthetic and educational** only.

## Ways to Contribute
- Improve documentation or add educational examples
- Enhance heuristic detectors or add synthetic datasets
- Expand tests and CI coverage
- Improve visualizations and UX for the dashboard

## Development Workflow
1. Fork and create a feature branch.
2. Install dependencies via `pip install -r requirements.txt`.
3. Run formatting and linting: `black . && isort . && ruff .`.
4. Run tests: `pytest`.
5. Submit a PR describing the changes and safety considerations (ensure synthetic scope).

## Code Style
- Follow PEP 8 and type hint everything.
- Keep functions small, named descriptively, and covered by docstrings.
- Avoid hard-coded secrets or production data.

## Safety
- Do not ingest or analyze real political content or real individuals.
- Keep all examples fictional and clearly labeled as synthetic.

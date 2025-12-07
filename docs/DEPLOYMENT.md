# Deployment & Operations Guide

## Local Development
- Install dependencies with `make install-dev` (preferred) or `pip install -r requirements-dev.txt`.
- Run the API: `make run` (uvicorn auto-reload can be toggled with `--reload`).
- Execute the dashboard by opening `frontend/index.html` and pointing requests at your API host.

## Containerized Run
```bash
docker compose up --build
```
- Builds the included `Dockerfile` and exposes the API on port `8000`.
- Health check is wired to `/health` via Docker Compose.
- The image pre-installs `en_core_web_sm` for spaCy to avoid runtime downloads.

## Production Considerations
- Place an HTTPS-capable reverse proxy (e.g., nginx/Traefik) in front of the container.
- Configure CORS allowlists per deployment rather than wildcard `*`.
- Add authentication/authorization middleware if multi-tenant usage is needed.
- Use read-only or tmpfs mounts for `logs/` and `reports/` when running in restricted environments.
- Pin dependency updates through `requirements*.txt` and rebuild regularly for security fixes.

## CI/CD
- GitHub Actions workflow (`.github/workflows/ci.yml`) executes linting and tests on every push/PR.
- Extend the workflow with image builds and vulnerability scanning (Trivy/Grype) for hardened pipelines.

## Backup & Retention
- Synthetic logs and reports are stored under `logs/` and `reports/` by default; rotate or purge regularly.
- Avoid persisting real user data—this project is intended for synthetic demonstrations only.

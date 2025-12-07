.PHONY: install install-dev lint format test run docker-up docker-down

install:
pip install -r requirements.txt

install-dev: install
pip install -r requirements-dev.txt

lint:
ruff check .
black . --check
isort . --check-only

format:
black .
isort .
ruff check . --fix

test:
pytest

run:
uvicorn backend.main:app --host 0.0.0.0 --port 8000

docker-up:
docker compose up --build -d

docker-down:
docker compose down

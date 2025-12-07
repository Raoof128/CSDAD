"""FastAPI application entrypoint for Cognitive Security Dashboard."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import image, risk, text, url
from .utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Synthetic Cognitive Security Dashboard",
    description=(
        "Educational demo for analyzing synthetic content across modalities."
        " No real-world political actors or individuals are processed."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(text.router)
app.include_router(image.router)
app.include_router(url.router)
app.include_router(risk.router)


@app.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe."""

    logger.info("Health check requested")
    return {"status": "ok"}


@app.get("/dashboard")
async def dashboard_summary() -> dict[str, str]:
    """Provide a summary for the dashboard front-end."""

    return {
        "message": "Synthetic Cognitive Security Dashboard ready.",
        "notice": "All analyses operate on fictional data for educational purposes only.",
    }

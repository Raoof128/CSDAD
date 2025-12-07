"""Visualization utilities for the dashboard."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from .logger import get_logger

logger = get_logger(__name__)
ASSETS_DIR = Path("reports")
ASSETS_DIR.mkdir(exist_ok=True)


def save_heatmap(matrix: np.ndarray, labels: List[str], name: str) -> str:
    """Save a similarity heatmap and return the file path as a string."""

    path = ASSETS_DIR / f"{name}_heatmap.png"
    try:
        plt.figure(figsize=(6, 5))
        sns.heatmap(matrix, xticklabels=labels, yticklabels=labels, cmap="magma")
        plt.tight_layout()
        plt.savefig(path)
        logger.info("Heatmap saved to %s", path)
        return str(path)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to save heatmap: %s", exc)
        raise
    finally:
        plt.close()


def save_timeline(series: Dict[str, float], name: str) -> str:
    """Save a simple timeline plot of influence scoring."""

    path = ASSETS_DIR / f"{name}_timeline.png"
    try:
        plt.figure(figsize=(6, 3))
        plt.plot(list(series.keys()), list(series.values()), marker="o")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(path)
        logger.info("Timeline saved to %s", path)
        return str(path)
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to save timeline: %s", exc)
        raise
    finally:
        plt.close()

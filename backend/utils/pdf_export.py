"""PDF report generator using synthetic analysis results."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from fpdf import FPDF

from .logger import get_logger

logger = get_logger(__name__)
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)


class ReportPDF(FPDF):
    """Simple PDF with header/footer for dashboard exports."""

    def header(self) -> None:  # type: ignore[override]
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Cognitive Security Synthetic Report", ln=True, align="C")
        self.ln(5)

    def footer(self) -> None:  # type: ignore[override]
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def build_report(
    summary: Dict[str, str],
    risks: Dict[str, float],
    recommendations: List[str],
    output_name: str = "report.pdf",
) -> str:
    """Create a PDF report from supplied data and return the path."""

    pdf = ReportPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    pdf.cell(0, 10, "Summary", ln=True)
    for key, value in summary.items():
        pdf.multi_cell(0, 8, f"- {key}: {value}")

    pdf.ln(4)
    pdf.cell(0, 10, "Risk Scores", ln=True)
    for key, score in risks.items():
        pdf.cell(0, 8, f"- {key}: {score:.1f}", ln=True)

    pdf.ln(4)
    pdf.cell(0, 10, "Recommended Actions", ln=True)
    for rec in recommendations:
        pdf.multi_cell(0, 8, f"• {rec}")

    output_path = REPORTS_DIR / output_name
    pdf.output(str(output_path))
    logger.info("PDF exported to %s", output_path)
    return str(output_path)

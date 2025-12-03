"""
Aetheron — PDF Utility Template
-------------------------------

This file provides a structural template for the PDF generation
module used across the Aetheron backend.

It is intended to demonstrate:

- How PDF building functions are organized
- How ReportLab structures are referenced
- How sections, headers, and layout components relate
- How a file-like buffer and filename are returned

All content generation, formatting rules, branding details, and
internal document structures have been simplified for template use.
"""

import io
import os
import time
import re

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Flowable,
)
from reportlab.lib import colors
from reportlab.lib.styles import StyleSheet1, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas


# -------------------------------------------------------------------------
# Color Palette (Template)
# -------------------------------------------------------------------------
PAGE_BG        = colors.HexColor("#FFFFFF")
ACCENT         = colors.HexColor("#6366F1")
ACCENT_SOFT    = colors.HexColor("#EEF2FF")
TEXT_MAIN      = colors.HexColor("#0F172A")
TEXT_MUTED     = colors.HexColor("#475569")
BORDER         = colors.HexColor("#E2E8F0")
CARD_BG        = colors.HexColor("#F8FAFC")
CODE_BG        = colors.HexColor("#F1F5F9")


# -------------------------------------------------------------------------
# Header + Footer Frames (Template)
# -------------------------------------------------------------------------

def _draw_page_frame(c: Canvas, title: str):
    """
    Draws a simple template header frame.
    The real backend uses a branded design.
    """
    w, h = c._pagesize
    c.saveState()

    # Header area
    c.setFillColor(colors.white)
    c.rect(0, h - 60, w, 60, fill=1, stroke=0)

    # Divider
    c.setStrokeColor(BORDER)
    c.setLineWidth(0.6)
    c.line(40, h - 60, w - 40, h - 60)

    # Title label
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(TEXT_MAIN)
    c.drawString(48, h - 45, title or "Aetheron Document")

    c.restoreState()


def _footer(c: Canvas, doc):
    """
    Draws a simple footer with page numbering.
    """
    w, h = c._pagesize
    c.saveState()

    c.setStrokeColor(BORDER)
    c.setLineWidth(0.5)
    c.line(52, 40, w - 48, 40)

    c.setFont("Helvetica", 7)
    c.setFillColor(TEXT_MUTED)

    c.drawString(52, 28, "Aetheron — Document")
    c.drawRightString(w - 48, 28, f"Page {doc.page}")

    c.restoreState()


# -------------------------------------------------------------------------
# Metric Card Flowable (Template)
# -------------------------------------------------------------------------

class MetricCard(Flowable):
    """
    Example metric card used to display scoring or small numeric details.

    Template version includes layout only.
    """

    def __init__(self, name: str, value: float, max_value=10):
        super().__init__()
        self.name = name
        self.value = value
        self.max_value = max_value
        self.width = 2.3 * inch
        self.height = 0.9 * inch

    def draw(self):
        c = self.canv

        c.setFillColor(CARD_BG)
        c.roundRect(0, 0, self.width, self.height, 6, fill=1, stroke=0)

        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(TEXT_MAIN)
        c.drawString(8, self.height - 18, self.name)

        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(ACCENT)
        c.drawString(8, self.height - 38, f"{self.value:.1f}")

        c.setFont("Helvetica", 7)
        c.setFillColor(TEXT_MUTED)
        c.drawString(8, 10, f"Out of {self.max_value}")


# -------------------------------------------------------------------------
# Radar Chart Placeholder (Template)
# -------------------------------------------------------------------------

def add_radar_chart(values, labels, size=200):
    """
    Template radar chart placeholder.
    In the full backend this generates a polygon radar graph.

    Template returns None to preserve structure.
    """
    return None


# -------------------------------------------------------------------------
# Main PDF Builder (Template)
# -------------------------------------------------------------------------

def build_aetheron_pdf(asset_id, timestamp, wallet, title, subtitle, md_text):
    """
    Template PDF generator.

    In the full backend:
    - Text is parsed into sections
    - Metrics are extracted
    - Charts, tables, and styled content are added
    - The PDF is rendered and uploaded for download

    Template version:
    - Produces a simple paragraph-based PDF
    - Returns (buffer, filename)
    """

    buffer = io.BytesIO()

    # Basic PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=60,
        leftMargin=72,
        topMargin=140,
        bottomMargin=60,
    )

    doc.title = title or "Aetheron Document"

    # Styles
    styles = StyleSheet1()
    styles.add(ParagraphStyle(name="Title", fontName="Helvetica-Bold", fontSize=18, textColor=TEXT_MAIN))
    styles.add(ParagraphStyle(name="Subtitle", fontName="Helvetica", fontSize=12, textColor=TEXT_MUTED))
    styles.add(ParagraphStyle(name="Body", fontName="Helvetica", fontSize=10, textColor=TEXT_MAIN, leading=15))

    story = []

    # Title Page (Template)
    story.append(Spacer(1, 0.8 * inch))
    story.append(Paragraph(title or "Aetheron Document", styles["Title"]))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph(subtitle or "", styles["Subtitle"]))
    story.append(PageBreak())

    # Simple text content
    clean_text = (md_text or "").strip()
    blocks = re.split(r"\n\s*\n", clean_text)

    for block in blocks:
        if not block.strip():
            continue
        story.append(Paragraph(block.replace("\n", "<br/>"), styles["Body"]))
        story.append(Spacer(1, 0.2 * inch))

    # Build the PDF
    doc.build(
        story,
        onFirstPage=lambda c, d: (_draw_page_frame(c, doc.title), _footer(c, d)),
        onLaterPages=lambda c, d: (_draw_page_frame(c, doc.title), _footer(c, d)),
    )

    buffer.seek(0)
    filename = f"aetheron_asset_{int(time.time())}.pdf"

    return buffer, filename

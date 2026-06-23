"""Generate the tiny PDF used by the first three RAG learning demos.

The PDF is intentionally short and synthetic. It exists to make the parsing
pipeline real without committing copyrighted paper content.
"""

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate


ROOT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT_DIR / "backend" / "app" / "sample_data" / "tiny_ablation_paper.pdf"


def build_pdf() -> None:
    """Write a stable two-page toy scientific PDF for parser demos."""

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TinyTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        spaceAfter=10,
    )
    heading = ParagraphStyle(
        "TinyHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        spaceBefore=10,
        spaceAfter=4,
    )
    body = ParagraphStyle(
        "TinyBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        spaceAfter=8,
    )

    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=A4,
        rightMargin=22 * mm,
        leftMargin=22 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="Tiny Ultrasound Thermometry Demo Paper",
        author="RAG Learning Lab",
    )

    story = [
        Paragraph("Tiny Ultrasound Thermometry Demo Paper", title),
        Paragraph("DOI: 10.0000/rag-learning-lab.2026.001", body),
        Paragraph("Year: 2026", body),
        Paragraph("Abstract", heading),
        Paragraph(
            "Thermal ablation procedures require reliable temperature monitoring because "
            "excess heating can damage surrounding tissue. This tiny teaching paper "
            "summarizes how ultrasound thermometry can support evidence-grounded RAG demos.",
            body,
        ),
        Paragraph("Methods", heading),
        Paragraph(
            "A compact literature-style note was written with page-level metadata. The "
            "demo parser extracts text from each PDF page, detects section names, cleans "
            "whitespace, and keeps DOI, year, page, and section metadata for citations.",
            body,
        ),
        PageBreak(),
        Paragraph("Discussion", heading),
        Paragraph(
            "Ultrasound thermometry may estimate temperature-related changes using speed "
            "of sound, attenuation, signal amplitude, and backscattered energy. The same "
            "parsed text can be chunked into retrieval units for later vector search.",
            body,
        ),
        Paragraph("Limitations", heading),
        Paragraph(
            "This PDF is synthetic and intentionally small. It demonstrates ingestion and "
            "debugging behavior, not clinical validity or a complete literature review.",
            body,
        ),
    ]
    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT_PATH)

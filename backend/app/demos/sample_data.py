# Tiny paper-like records used across the demos. The fields mirror the final
# project's citation metadata, but the text is intentionally short for debugging.
TOY_PAPERS = [
    {
        "doc_id": "paper_001",
        "title": "2D ultrasound thermometry during thermal ablation with HIFU",
        "doi": "10.1016/j.ultras.2024.107372",
        "year": 2024,
        "section": "Discussion",
        "page": 8,
        "text": (
            "Ultrasound thermometry estimates temperature change during thermal ablation "
            "using speed of sound, elasticity, attenuation, signal amplitude, and "
            "backscattered energy. Temperature measurements are most reliable in a limited "
            "range and may be affected by tissue coagulation."
        ),
    },
    {
        "doc_id": "paper_002",
        "title": "Dual-layer spectral CT for in vivo thermometry during thermal ablation",
        "doi": "10.1007/s00270-025-04316-z",
        "year": 2026,
        "section": "Methods",
        "page": 3,
        "text": (
            "Dual-layer spectral CT can estimate temperature through electron-density "
            "weighted imaging and effective atomic number. The method is promising for "
            "non-invasive thermometry but still requires animal-model validation."
        ),
    },
    {
        "doc_id": "paper_003",
        "title": "MR thermometry for focused ultrasound therapy monitoring",
        "doi": "10.1148/radiol.2023.demo",
        "year": 2023,
        "section": "Results",
        "page": 5,
        "text": (
            "MRI thermometry provides non-invasive temperature maps during focused "
            "ultrasound therapy. It offers strong spatial temperature monitoring, but "
            "equipment cost and compatibility can limit clinical deployment."
        ),
    },
    {
        "doc_id": "paper_004",
        "title": "Thermocouple validation during microwave ablation",
        "doi": "10.1109/tmi.2022.demo",
        "year": 2022,
        "section": "Experiment",
        "page": 4,
        "text": (
            "Thermocouples can be placed directly into an ablation region to measure local "
            "temperature. This invasive reference is useful for validation but may disturb "
            "the tissue and does not provide a full temperature map."
        ),
    },
]

SIMULATED_PDF_PAGES = [
    {
        "page": 1,
        "raw_text": (
            "Title: Ultrasound-guided ablation monitoring\n"
            "Abstract\n"
            "Temperature monitoring is important during thermal ablation."
        ),
    },
    {
        "page": 2,
        "raw_text": (
            "Discussion\n"
            "Ultrasound-based thermometry can use speed of sound and backscatter changes. "
            "The method is sensitive to tissue state and acquisition settings."
        ),
    },
]

EVALUATION_SET = [
    {
        "question": "Which methods can monitor temperature during thermal ablation?",
        "relevant_chunk_ids": ["paper_001_c001", "paper_002_c001", "paper_003_c001"],
        "required_claims": ["ultrasound", "spectral CT", "MRI"],
    },
    {
        "question": "What is a limitation of thermocouple monitoring?",
        "relevant_chunk_ids": ["paper_004_c001"],
        "required_claims": ["invasive"],
    },
    {
        "question": "Why is spectral CT not yet fully established?",
        "relevant_chunk_ids": ["paper_002_c001"],
        "required_claims": ["validation"],
    },
]


def paper_chunks() -> list[dict]:
    """Convert toy papers into chunk records shared by retrieval demos.

    Each returned chunk has:
    - chunk_id: stable retrieval/evaluation identifier.
    - content: text that can be embedded or keyword-scored.
    - metadata: citation fields shown in evidence cards.
    """

    chunks = []
    for paper in TOY_PAPERS:
        chunk = {
            "chunk_id": f"{paper['doc_id']}_c001",
            "doc_id": paper["doc_id"],
            "content": paper["text"],
            "metadata": {
                "title": paper["title"],
                "doi": paper["doi"],
                "year": paper["year"],
                "section": paper["section"],
                "page": paper["page"],
            },
        }
        chunks.append(chunk)
    return chunks

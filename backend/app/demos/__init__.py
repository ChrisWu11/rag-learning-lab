from backend.app.demos import (
    chunking,
    corpus_metadata,
    embeddings,
    evaluation,
    grounded_generation,
    hybrid_retrieval,
    image_qa,
    pdf_parsing,
    reranking,
)

DEMO_REGISTRY = {
    "corpus_metadata": corpus_metadata.run,
    "pdf_parsing": pdf_parsing.run,
    "chunking": chunking.run,
    "embeddings": embeddings.run,
    "hybrid_retrieval": hybrid_retrieval.run,
    "reranking": reranking.run,
    "grounded_generation": grounded_generation.run,
    "evaluation": evaluation.run,
}

DEMO_LIST = [
    {
        "id": "corpus_metadata",
        "title": "01 Corpus & Metadata",
        "description": "Why private scientific corpora need DOI, page, section, and chunk IDs.",
        "route": "/corpus-metadata",
    },
    {
        "id": "pdf_parsing",
        "title": "02 PDF Parsing",
        "description": "Extract page text and keep citation-ready page context.",
        "route": "/pdf-parsing",
    },
    {
        "id": "chunking",
        "title": "03 Chunking",
        "description": "Split scientific text into retrieval-ready chunks with overlap.",
        "route": "/chunking",
    },
    {
        "id": "embeddings",
        "title": "04 Embedding & Vector Search",
        "description": "Use Gemini embeddings and cosine similarity for semantic retrieval.",
        "route": "/embeddings",
    },
    {
        "id": "hybrid_retrieval",
        "title": "05 Hybrid Retrieval",
        "description": "Fuse keyword and vector rankings for stronger scientific retrieval.",
        "route": "/hybrid-retrieval",
    },
    {
        "id": "reranking",
        "title": "06 Reranking",
        "description": "Reorder top-k candidates using query-evidence relevance scoring.",
        "route": "/reranking",
    },
    {
        "id": "grounded_generation",
        "title": "07 Grounded Generation",
        "description": "Generate a cited answer constrained by retrieved evidence.",
        "route": "/grounded-generation",
    },
    {
        "id": "image_qa",
        "title": "08 Image Question Answering",
        "description": "Use Gemini Vision to summarize an image before literature retrieval.",
        "route": "/image-qa",
    },
    {
        "id": "evaluation",
        "title": "09 Evaluation",
        "description": "Evaluate retrieval, reranking, generation faithfulness, and citation support.",
        "route": "/evaluation",
    },
]


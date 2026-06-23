import base64
import math
import re
from collections import Counter
from typing import Any

import numpy as np
from google import genai
from google.genai import types

from backend.app.config import get_settings


def tokenize(text: str) -> list[str]:
    """Normalize text into simple lowercase tokens for toy lexical scoring."""

    return re.findall(r"[a-zA-Z][a-zA-Z0-9-]+", text.lower())


def keyword_score(query: str, text: str) -> float:
    """Return the fraction of query terms that also appear in a candidate chunk.

    Args:
        query: User question or expanded retrieval query.
        text: Candidate chunk content to compare against the query.
    """

    query_terms = set(tokenize(query))
    text_terms = set(tokenize(text))
    if not query_terms:
        return 0.0
    return len(query_terms & text_terms) / len(query_terms)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Measure vector similarity between a query embedding and a chunk embedding."""

    va = np.array(a, dtype=float)
    vb = np.array(b, dtype=float)
    denom = np.linalg.norm(va) * np.linalg.norm(vb)
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)


def fallback_embedding(text: str, dimensions: int = 32) -> list[float]:
    """Create a deterministic local vector when Gemini is disabled or unavailable.

    Args:
        text: Text to convert into a toy vector.
        dimensions: Size of the small hashed vector. Kept low so it is easy to inspect.
    """

    counts = Counter(tokenize(text))
    vector = [0.0] * dimensions
    for term, count in counts.items():
        vector[hash(term) % dimensions] += float(count)
    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [round(value / norm, 6) for value in vector]


class GeminiService:
    """Thin wrapper around Gemini calls used by the demos.

    Keeping Gemini access here makes the API key backend-only and gives every demo
    the same fallback/error behavior.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.client = (
            genai.Client(api_key=self.settings.gemini_api_key)
            if self.settings.gemini_api_key and not self.settings.disable_gemini
            else None
        )

    def require_client(self) -> genai.Client:
        """Return an initialized Gemini client or raise a learner-friendly error."""

        if not self.client:
            raise RuntimeError(
                "Gemini is unavailable. Add GEMINI_API_KEY to .env, or set DISABLE_GEMINI=false, "
                "then restart the backend."
            )
        return self.client

    def _extract_embedding_vectors(self, response: Any) -> list[list[float]]:
        """Normalize single-item and batch embedding responses into one list shape."""

        vectors = []
        for item in getattr(response, "embeddings", None) or []:
            vectors.append([float(value) for value in item.values])
        single_embedding = getattr(response, "embedding", None)
        if single_embedding is not None:
            vectors.append([float(value) for value in single_embedding.values])
        return vectors

    def embed_texts(self, texts: list[str]) -> tuple[list[list[float]], dict[str, Any]]:
        """Embed a list of texts with Gemini.

        Args:
            texts: First item is usually the query; remaining items are candidate chunks.

        Returns:
            A pair of embedding vectors and metadata about the provider/model.
        """

        client = self.require_client()
        response = client.models.embed_content(
            model=self.settings.gemini_embedding_model,
            contents=texts,
        )
        vectors = self._extract_embedding_vectors(response)
        if len(vectors) != len(texts):
            # Some Gemini model/API combinations return only one vector for a list input.
            # Retrying item-by-item keeps this learning demo stable and easier to debug.
            vectors = []
            for text in texts:
                item_response = client.models.embed_content(
                    model=self.settings.gemini_embedding_model,
                    contents=text,
                )
                item_vectors = self._extract_embedding_vectors(item_response)
                if not item_vectors:
                    raise RuntimeError("Gemini embedding response did not include vectors.")
                vectors.append(item_vectors[0])
        return vectors, {
            "provider": "gemini",
            "model": self.settings.gemini_embedding_model,
            "dimensions": len(vectors[0]) if vectors else 0,
        }

    def generate_text(self, prompt: str) -> dict[str, Any]:
        """Generate a grounded answer from a prompt that already contains evidence."""

        client = self.require_client()
        response = client.models.generate_content(
            model=self.settings.gemini_text_model,
            contents=prompt,
        )
        return {
            "provider": "gemini",
            "model": self.settings.gemini_text_model,
            "text": response.text or "",
        }

    def summarize_image(self, image_bytes: bytes, mime_type: str, question: str) -> dict[str, Any]:
        """Ask Gemini Vision for a question-aware image summary.

        Args:
            image_bytes: Raw uploaded image bytes.
            mime_type: Browser-provided MIME type, validated before this method is called.
            question: User question used to focus the visual summary on retrieval terms.
        """

        client = self.require_client()
        prompt = (
            "You are helping a RAG learning demo. Describe only visible image evidence. "
            "Do not diagnose. Extract retrieval terms relevant to this question: "
            f"{question}\n\nReturn concise bullets with headings: Image type, Observable "
            "features, Uncertainty, Retrieval terms."
        )
        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        response = client.models.generate_content(
            model=self.settings.gemini_vision_model,
            contents=[prompt, image_part],
        )
        return {
            "provider": "gemini",
            "model": self.settings.gemini_vision_model,
            "text": response.text or "",
            "image_size_bytes": len(image_bytes),
            "mime_type": mime_type,
            "image_preview_base64": base64.b64encode(image_bytes[:24]).decode("ascii"),
        }


def safe_gemini_call(callback, fallback: Any | None = None) -> tuple[Any, dict[str, Any]]:
    """Run a Gemini call and return status metadata instead of crashing the UI."""

    try:
        return callback(), {"ok": True, "error": None}
    except Exception as exc:  # noqa: BLE001 - returned for learning/debugging
        return fallback, {"ok": False, "error": str(exc)}


def format_citation(chunk: dict, index: int) -> dict[str, Any]:
    """Convert a retrieved chunk into the citation-card shape used by the frontend."""

    metadata = chunk["metadata"]
    return {
        "citation_id": index,
        "chunk_id": chunk["chunk_id"],
        "title": metadata["title"],
        "doi": metadata["doi"],
        "page": metadata["page"],
        "section": metadata["section"],
    }

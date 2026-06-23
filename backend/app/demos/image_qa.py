from fastapi import UploadFile

from backend.app.demos.grounded_generation import build_prompt, extractive_fallback, select_evidence
from backend.app.demos.utils import GeminiService, format_citation, safe_gemini_call
from backend.app.schemas import DemoResponse, DemoStep

ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/webp"}


async def run_image_demo(question: str, image: UploadFile, options: dict) -> DemoResponse:
    """Run the image-grounded RAG demo.

    Args:
        question: User question about the uploaded image and related literature.
        image: Uploaded image file from the multipart request.
        options: Supports top_k, which controls how many paper chunks are retrieved.
    """

    image_bytes = await image.read()
    mime_type = image.content_type or "application/octet-stream"
    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError("Only PNG, JPEG, and WebP images are supported in this demo.")
    if len(image_bytes) > 5 * 1024 * 1024:
        raise ValueError("Image is too large for this learning demo. Use an image under 5 MB.")

    service = GeminiService()
    # Step 1: convert the image into text so the normal text retriever can use it.
    image_summary, vision_status = safe_gemini_call(
        lambda: service.summarize_image(image_bytes, mime_type, question),
        fallback={
            "provider": "none",
            "model": None,
            "text": "Image summary unavailable because Gemini Vision did not complete.",
            "image_size_bytes": len(image_bytes),
            "mime_type": mime_type,
        },
    )
    # Step 2: combine user intent and visual observations into one retrieval query.
    expanded_query = f"{question}\n\nImage observations:\n{image_summary['text']}"
    evidence = select_evidence(expanded_query, int(options.get("top_k", 3)))
    prompt = (
        "The answer has two evidence types. Use [Image] for visible observations and "
        "numbered citations [1], [2] only for literature evidence.\n\n"
        f"Image summary:\n{image_summary['text']}\n\n"
        f"{build_prompt(question, evidence)}"
    )
    generated, generation_status = safe_gemini_call(
        lambda: service.generate_text(prompt),
        fallback={"provider": "extractive_fallback", "model": None, "text": extractive_fallback(question, evidence)},
    )

    return DemoResponse(
        demo_id="image_qa",
        title="08 Image Question Answering",
        concept=(
            "Image QA first turns the uploaded image into a question-aware text summary. "
            "That summary expands the retrieval query before grounded answer generation."
        ),
        steps=[
            DemoStep(
                name="uploaded_image",
                output={"filename": image.filename, "mime_type": mime_type, "size_bytes": len(image_bytes)},
            ),
            DemoStep(name="gemini_vision_summary", output={**image_summary, "status": vision_status}),
            DemoStep(name="expanded_retrieval_query", output=expanded_query),
            DemoStep(name="retrieved_literature_evidence", output=evidence),
            DemoStep(name="generation_status", output=generation_status),
        ],
        final_output={
            "answer": generated["text"],
            "provider": generated["provider"],
            "model": generated["model"],
            "sources": [format_citation(chunk, index) for index, chunk in enumerate(evidence, start=1)],
        },
        interview_notes=[
            "The image itself is not treated as a paper citation; it is labelled separately as image observation.",
            "The visual summary improves retrieval by adding image-derived terms to the query.",
        ],
    )

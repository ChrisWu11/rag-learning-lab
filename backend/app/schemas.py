from typing import Any

from pydantic import BaseModel, Field


class DemoRequest(BaseModel):
    """Common JSON request body for text-only demos."""

    question: str = Field(
        default="What temperature monitoring methods are used during thermal ablation?",
        description="User question sent to the selected demo pipeline.",
    )
    options: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Demo-specific controls such as top_k, chunk_size, and overlap. "
            "Each demo reads only the options it needs."
        ),
    )


class DemoStep(BaseModel):
    """One visible intermediate step shown in the frontend debugger."""

    name: str = Field(description="Stable step name used by the UI.")
    output: Any = Field(description="JSON-serializable intermediate result for inspection.")


class DemoResponse(BaseModel):
    """Standard response shape returned by every learning demo."""

    demo_id: str = Field(description="Identifier of the demo that produced this response.")
    title: str = Field(description="Human-readable demo title.")
    concept: str = Field(description="Short explanation of the RAG concept being demonstrated.")
    steps: list[DemoStep] = Field(description="Ordered intermediate outputs for debugging.")
    final_output: Any = Field(description="The final result the learner should focus on.")
    interview_notes: list[str] = Field(description="Concise talking points for interviews.")


class DemoMeta(BaseModel):
    """Navigation metadata used by the React sidebar."""

    id: str = Field(description="Demo identifier used in API routes.")
    title: str = Field(description="Sidebar title.")
    description: str = Field(description="Short sidebar description.")
    route: str = Field(description="Frontend hash route for this demo.")

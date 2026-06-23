from typing import Any

from pydantic import BaseModel, Field


class DemoRequest(BaseModel):
    question: str = Field(
        default="What temperature monitoring methods are used during thermal ablation?"
    )
    options: dict[str, Any] = Field(default_factory=dict)


class DemoStep(BaseModel):
    name: str
    output: Any


class DemoResponse(BaseModel):
    demo_id: str
    title: str
    concept: str
    steps: list[DemoStep]
    final_output: Any
    interview_notes: list[str]


class DemoMeta(BaseModel):
    id: str
    title: str
    description: str
    route: str


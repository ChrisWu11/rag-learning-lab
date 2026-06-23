from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from backend.app.demos import DEMO_LIST, DEMO_REGISTRY
from backend.app.demos.image_qa import run_image_demo
from backend.app.schemas import DemoMeta, DemoRequest, DemoResponse

app = FastAPI(title="RAG Learning Lab", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/demos", response_model=list[DemoMeta])
def demos() -> list[dict]:
    return DEMO_LIST


@app.post("/api/demos/{demo_id}/run", response_model=DemoResponse)
def run_demo(demo_id: str, request: DemoRequest) -> DemoResponse:
    if demo_id not in DEMO_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Unknown demo: {demo_id}")
    return DEMO_REGISTRY[demo_id](request.question, request.options)


@app.post("/api/demos/image_qa/run", response_model=DemoResponse)
async def run_image_qa(
    question: str = Form(...),
    top_k: int = Form(3),
    image: UploadFile = File(...),
) -> DemoResponse:
    try:
        return await run_image_demo(question, image, {"top_k": top_k})
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


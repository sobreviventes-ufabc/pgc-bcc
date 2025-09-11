from fastapi import FastAPI
from pydantic import BaseModel
import anyio
from core.retriever_pipeline import get_rag_pipeline

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.on_event("startup")
def build_pipeline_once():
    # instancia uma única vez por processo/worker
    app.state.pipeline = get_rag_pipeline(force_regenerate=False)

@app.post("/ask")
async def ask_question(req: QueryRequest):
    pipeline = app.state.pipeline
    # .invoke é bloqueante: manda pra thread pool
    resp = await anyio.to_thread.run_sync(pipeline.invoke, req.question)
    return {
        "response": resp["response"],
        "context": {
            "texts": resp["context"]["texts"],
            "images": resp["context"]["images"],
        },
    }

@app.get("/health")
def health():
    return {"ok": True}
from fastapi import FastAPI
from pydantic import BaseModel
import anyio
from core.retriever_pipeline import get_rag_pipeline
from contextlib import asynccontextmanager

class QueryRequest(BaseModel):
    question: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # instancia uma única vez por processo/worker
    app.state.pipeline = get_rag_pipeline(force_regenerate=False)
    yield

app = FastAPI(lifespan=lifespan)

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
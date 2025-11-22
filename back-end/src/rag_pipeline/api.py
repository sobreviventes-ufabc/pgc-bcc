from fastapi import FastAPI, Header
import uvicorn
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal, Optional
import anyio
from .core.retriever_pipeline import get_rag_pipeline
from contextlib import asynccontextmanager

class QueryRequest(BaseModel):
    question: str

class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # instancia uma única vez por processo/worker
    app.state.pipeline = get_rag_pipeline(force_regenerate=False)
    yield


app = FastAPI(lifespan=lifespan)

handler = Mangum(app)  # Entry point for AWS Lambda.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask")
async def ask_question(req: QueryRequest, include_context: Optional[str] = Header(default="true")):
    pipeline = app.state.pipeline
    question = f"Pergunta: {req.question}"

    # .invoke é bloqueante: manda pra thread pool
    resp = await anyio.to_thread.run_sync(pipeline.invoke, question)
    
    # Check if context should be included (default: true)
    should_include_context = include_context.lower() in ("true", "1", "yes")
    
    result = {"response": resp["response"]}
    if should_include_context:
        result["context"] = {
            "texts": resp["context"]["texts"],
            "images": resp["context"]["images"],
        }
    
    return result


# --- Novo endpoint /chat ---

@app.post("/chat")
async def chat(req: ChatRequest, include_context: Optional[str] = Header(default="true")):
    try:
        pipeline = app.state.pipeline
        # Separa histórico e pergunta atual
        history = []
        for m in req.messages[:-1]:
            if m.role in ("system", "user"):
                history.append(f"{m.role}: {m.content}")
        historico_str = "\n".join(history) if history else None
        
        ultima_msg = req.messages[-1]
        question = ultima_msg.content
        
        # Envia pergunta e histórico separadamente para o pipeline
        resp = await anyio.to_thread.run_sync(
            pipeline.invoke, 
            {"question": f"Pergunta: {question}", "history": historico_str}
        )
        
        # Check if context should be included (default: true)
        should_include_context = include_context.lower() in ("true", "1", "yes")
        
        result = {"response": resp["response"]}
        if should_include_context:
            result["context"] = {
                "texts": resp["context"]["texts"],
                "images": resp["context"]["images"],
            }
        
        return result
    except Exception as e:
        print(f"Error in /chat endpoint: {type(e).__name__}: {str(e)}")
        raise


@app.get("/health")
def health():
    return {"ok": True}

if __name__ == "__main__":
    # Run this as a server directly.
    port = 8000
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("rag_pipeline.api:app", host="0.0.0.0", port=port)
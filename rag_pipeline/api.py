from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal
import anyio
from core.retriever_pipeline import get_rag_pipeline
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/ask")
async def ask_question(req: QueryRequest):
    pipeline = app.state.pipeline
    question = f"Pergunta: {req.question}"

    # .invoke é bloqueante: manda pra thread pool
    resp = await anyio.to_thread.run_sync(pipeline.invoke, question)
    return {
        "response": resp["response"],
        "context": {
            "texts": resp["context"]["texts"],
            "images": resp["context"]["images"],
        },
    }


# --- Novo endpoint /chat ---

@app.post("/chat")
async def chat(req: ChatRequest):
    pipeline = app.state.pipeline
    # Junta todas as mensagens (system e user) como contexto
    # Formata como um histórico de conversa para o modelo
    # Separa histórico e pergunta atual
    history = []
    for m in req.messages[:-1]:
        if m.role in ("system", "user"):
            history.append(f"{m.role}: {m.content}")
    historico_str = "\n".join(history)
    ultima_msg = req.messages[-1]
    pergunta_str = f"{ultima_msg.role}: {ultima_msg.content}" if ultima_msg.role in ("system", "user") else ""
    conversation = f"Histórico da conversa:\n{historico_str}\n\nPergunta: {pergunta_str}"

    print(conversation)
    # Envia o histórico completo para o pipeline
    resp = await anyio.to_thread.run_sync(pipeline.invoke, conversation)
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
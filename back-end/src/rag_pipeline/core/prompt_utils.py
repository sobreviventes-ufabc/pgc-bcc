from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage

# core/prompt_utils.py (ou onde estiver o parse_docs)
import base64
import re
from base64 import b64decode

_B64_RE = re.compile(r'^[A-Za-z0-9+/]+={0,2}$')

def _looks_like_base64(s: str) -> bool:
    if not isinstance(s, str):
        return False
    if len(s) < 100:
        return False
    if len(s) % 4 != 0:
        return False
    if not _B64_RE.match(s):
        return False
    try:
        base64.b64decode(s, validate=True)
        return True
    except Exception:
        return False

def parse_docs(docs):
    b64_imgs, texts = [], []
    for doc in docs:
        # docstore -> bytes; converte pra str
        if isinstance(doc, (bytes, bytearray)):
            doc = doc.decode("utf-8", errors="ignore")

        if _looks_like_base64(doc):
            b64_imgs.append(doc)
        else:
            texts.append(doc)
    return {"images": b64_imgs, "texts": texts}

def build_prompt(kwargs):
    docs = kwargs["context"]
    question = kwargs["question"]
    context_text = "".join(docs["texts"])
    prompt_content = [
        {"type": "text", "text": f"""
        Responda à pergunta usando apenas e exclusivamente o seguinte contexto e o histórico da conversa, sem pesquisas adicionais. 
        De preferencia para responder usando o contexto. Use algo do histórico da conversa somente se for solicitado.

        Contexto: {context_text}
        
        {question}

        Formate a resposta em HTML. Vou usar esse HTML para injetar diretamente em um componente react usando dangerouslySetInnerHTML.
        """}
    ]
    for image in docs["images"]:
        prompt_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})
    return ChatPromptTemplate.from_messages([HumanMessage(content=prompt_content)])

def clean_summary(text):
    return text.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\').strip()
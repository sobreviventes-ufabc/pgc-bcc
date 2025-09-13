import os
from pathlib import Path

# CONFIG
os.environ["GROQ_API_KEY"] = "gsk_2dNbVsmRut4gCoos4ePGWG..."
os.environ["OPENAI_API_KEY"] = "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"

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_DIR = (BASE_DIR / "data_extraction" / "test").resolve()
# PDF_DIR = (BASE_DIR / "data_extraction" / "documentos_ufabc" / "Prograd" / "Sobre" / "Apresentacoes").resolve()
CHUNKS_PATH = (BASE_DIR / ".cache_chunks" / "chunks_classificados.json").resolve()
SUMMARIES_PATH = (BASE_DIR / ".cache_chunks" / "summaries.json").resolve()
CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)

PERSIST_DIR = (BASE_DIR / ".cache_chunks" / "chroma_store").resolve()
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

MAX_WORKERS = min(10, os.cpu_count() or 4)
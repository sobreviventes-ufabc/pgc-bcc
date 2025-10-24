import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # Only loads if file exists, doesn't override existing env vars

required_env_vars = ["GROQ_API_KEY", "OPENAI_API_KEY", "OLLAMA_BASE_URL"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "ollama").lower()
valid_providers = ["ollama", "openai", "groq"]
if MODEL_PROVIDER not in valid_providers:
    raise ValueError(f"Invalid MODEL_PROVIDER '{MODEL_PROVIDER}'. Must be one of: {', '.join(valid_providers)}")

PDF_DIR = (BASE_DIR / "data_extraction" / "documentos_ufabc").resolve()
CHUNKS_PATH = (BASE_DIR / ".cache_chunks" / "chunks_classificados.json").resolve()
SUMMARIES_PATH = (BASE_DIR / ".cache_chunks" / "summaries.json").resolve()
CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)

PERSIST_DIR = (BASE_DIR / ".cache_chunks" / "chroma_store").resolve()
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

MAX_WORKERS = min(10, os.cpu_count() or 4)
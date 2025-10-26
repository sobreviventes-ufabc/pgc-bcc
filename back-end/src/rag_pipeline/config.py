import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

IS_USING_IMAGE_RUNTIME = bool(os.environ.get("IS_USING_IMAGE_RUNTIME", False))
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_PARENT_DIR = Path(__file__).resolve().parent.parent.parent

# Only load .env file if not in Lambda environment
if not IS_USING_IMAGE_RUNTIME:
    load_dotenv(SRC_PARENT_DIR / ".env")  # Loads .env from parent of src

# For Lambda, environment variables are already set via CDK
# For local development, they come from .env file
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") 
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
NOMIC_KEY = os.getenv("NOMIC_KEY")

required_env_vars = ["GROQ_API_KEY", "OLLAMA_BASE_URL"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

MODEL_PROVIDER = os.getenv("MODEL_PROVIDER")
valid_providers = ["ollama", "openai", "groq"]
if MODEL_PROVIDER not in valid_providers:
    raise ValueError(f"Invalid MODEL_PROVIDER '{MODEL_PROVIDER}'. Must be one of: {', '.join(valid_providers)}")

EMBEDDINGS_PROVIDER = os.getenv("EMBEDDINGS_PROVIDER", "ollama").lower()
valid_embedding_providers = ["ollama", "nomic"]
if EMBEDDINGS_PROVIDER not in valid_embedding_providers:
    raise ValueError(f"Invalid EMBEDDINGS_PROVIDER '{EMBEDDINGS_PROVIDER}'. Must be one of: {', '.join(valid_embedding_providers)}")

PDF_DIR = (BASE_DIR / "data_extraction" / "documentos_ufabc").resolve()
CHUNKS_PATH = (BASE_DIR / ".cache_chunks" / "chunks_classificados.json").resolve()
SUMMARIES_PATH = (BASE_DIR / ".cache_chunks" / "summaries.json").resolve()
CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)

PERSIST_DIR = (BASE_DIR / ".cache_chunks" / "chroma_store").resolve()
PERSIST_DIR.mkdir(parents=True, exist_ok=True)

MAX_WORKERS = min(10, os.cpu_count() or 4)

WORKER_LAMBDA_NAME = os.environ.get("WORKER_LAMBDA_NAME", None)

def copy_chroma_to_tmp():
    dst_chroma_path = get_runtime_chroma_path()

    if not os.path.exists(dst_chroma_path):
        os.makedirs(dst_chroma_path)

    tmp_contents = os.listdir(dst_chroma_path)
    if len(tmp_contents) == 0:
        print(f"Copying ChromaDB from {PERSIST_DIR} to {dst_chroma_path}")
        os.makedirs(dst_chroma_path, exist_ok=True)
        shutil.copytree(PERSIST_DIR, dst_chroma_path, dirs_exist_ok=True)
    else:
        print(f"✅ ChromaDB already exists in {dst_chroma_path}")

def get_runtime_chroma_path():
    if IS_USING_IMAGE_RUNTIME:
        return f"/tmp/{str(PERSIST_DIR)}"
    else:
        return str(PERSIST_DIR)

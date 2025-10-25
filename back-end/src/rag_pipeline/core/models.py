from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_ollama.embeddings import OllamaEmbeddings
from core.nomic_embeddings import NomicEmbeddings
from config import OLLAMA_BASE_URL, MODEL_PROVIDER, EMBEDDINGS_PROVIDER, NOMIC_KEY

def get_llava_model():
    try:
        model = ChatOllama(model="llava:13b", base_url=OLLAMA_BASE_URL).bind()
        print("Usando modelo local para imagens: llava:13b")
        return model
    except Exception as e:
        raise RuntimeError(f"Erro ao iniciar modelo llava: {e}")

def get_llama_model():
    if MODEL_PROVIDER == "ollama":
        try:
            model = ChatOllama(model="llama3.1:8b", base_url=OLLAMA_BASE_URL).bind()
            print("Usando modelo Ollama para texto: llama3.1:8b")
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao usar modelo Ollama: {e}")
    
    if MODEL_PROVIDER == "openai":
        try:
            model = ChatOpenAI(model="gpt-4o-mini")
            print("Usando modelo OpenAI: gpt-4o-mini")
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao usar modelo OpenAI: {e}")
    
    if MODEL_PROVIDER == "groq":
        try:
            model = ChatGroq(model="llama-3.1-8b-instant")
            print("Usando modelo Groq: llama-3.1-8b-instant")
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao usar modelo Groq: {e}")
    
    raise RuntimeError(f"Provedor de modelo inválido: {MODEL_PROVIDER}")

def get_embeddings_model():
    """
    Retorna o modelo de embeddings baseado na variável de ambiente EMBEDDINGS_PROVIDER.
    Opções: 'ollama' (padrão) ou 'nomic'.
    """
    if EMBEDDINGS_PROVIDER == "ollama":
        try:
            model = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)
            print("Usando Ollama para embeddings: nomic-embed-text")
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao usar Ollama embeddings: {e}")
    
    if EMBEDDINGS_PROVIDER == "nomic":
        if not NOMIC_KEY:
            raise RuntimeError("NOMIC_KEY não configurado. Defina a variável de ambiente NOMIC_KEY para usar Nomic API.")
        try:
            model = NomicEmbeddings(api_key=NOMIC_KEY)
            print("Usando Nomic API para embeddings: nomic-embed-text-v1.5")
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao usar Nomic API embeddings: {e}")
    
    raise RuntimeError(f"Provedor de embeddings inválido: {EMBEDDINGS_PROVIDER}")

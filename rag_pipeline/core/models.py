import os
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI

def get_llava_model():
    try:
        model = ChatOllama(model="llava:13b", base_url=os.getenv("OLLAMA_BASE_URL")).bind()
        print("Usando modelo local para imagens: llava:13b")
        return model
    except Exception as e:
        raise RuntimeError(f"Erro ao iniciar modelo llava: {e}")

def get_llama_model():
    model_provider = os.getenv("MODEL_PROVIDER", "ollama").lower()
    
    if model_provider == "ollama":
        try:
            model = ChatOllama(model="llama3.1:8b", base_url=os.getenv("OLLAMA_BASE_URL")).bind()
            print("Usando modelo Ollama para texto: llama3.1:8b")
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao usar modelo Ollama: {e}")
    
    if model_provider == "openai":
        try:
            model = ChatOpenAI(model="gpt-4o-mini")
            print("Usando modelo OpenAI: gpt-4o-mini")
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao usar modelo OpenAI: {e}")
    
    if model_provider == "groq":
        try:
            model = ChatGroq(model="llama3-8b-8192")
            print("Usando modelo Groq: llama3-8b-8192")
            return model
        except Exception as e:
            raise RuntimeError(f"Erro ao usar modelo Groq: {e}")
    
    raise RuntimeError(f"Provedor de modelo inválido: {model_provider}")
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
import os

def get_llava_model():
    try:
        model = ChatOllama(model="llava:13b", base_url="http://localhost:11434").bind()
        print("Usando modelo local remoto para imagens: llava:13b")
        return model
    except Exception as e:
        raise RuntimeError(f"Erro ao iniciar modelo llava: {e}")

def  get_llama_model():
    try:


        os.environ["OPENAI_API_KEY"] = "123"
        
        model = ChatOpenAI(model="gpt-4o")
        print("Usando modelo via OpenAI: gpt-4o")
        # model = ChatOllama(model="llama3.2:3b", base_url="http://localhost:11434").bind()
        # print("Usando modelo local remoto para texto: llama3.2:3b")
        return model
    except Exception:
        try:
            model = ChatGroq(model="llama3-8b-8192")
            print("Usando modelo via Groq: llama3-8b-8192")
            return model
        except Exception:
            model = ChatOpenAI(model="gpt-4o-mini")
            print("Usando modelo via OpenAI: gpt-4o-mini")
            return model
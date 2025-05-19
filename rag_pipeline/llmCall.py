import requests

OLLAMA_URL = "http://192.168.18.9:11434/api/chat" 

def send_prompt_to_llm(prompt, model="llama3:8b"):
    if isinstance(prompt, str):
        messages = [
            {"role": "system", "content": "Você é um assistente útil."}, #e só deve responder com base no contexto fornecido.
            {"role": "user", "content": prompt}
        ]
    else:
        messages = prompt  # já vem estruturado

    payload = {
        "model": model,
        "messages": messages,
        "stream": False  # estilo gpt seria true
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        print(f"Erro ao consultar Ollama: {e}")
        return "Erro ao gerar resposta com o modelo."
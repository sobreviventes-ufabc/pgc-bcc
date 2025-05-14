import openai

from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",  # ou https://api.groq.com/openai/v1
    api_key="substituirpelachave"
)

def send_prompt_to_llm(prompt, model="meta-llama/Llama-3.1-8B-Instruct"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Você é um assistente que responde apenas com base nos documentos fornecidos."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
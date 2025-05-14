def build_rag_prompt(context_chunks, question):
    context_text = "\n\n".join(context_chunks)
    return f"""
Você é um assistente altamente treinado para responder perguntas com base em documentos fornecidos.

Contexto:
{context_text}

Pergunta:
{question}

Responda de forma clara e objetiva.
"""
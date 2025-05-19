# 🤖 Chatbot Assistente UFABC

Este repositório contém o desenvolvimento de um **chatbot assistente para a UFABC**, utilizando a arquitetura de **Retrieval-Augmented Generation (RAG)**. O objetivo do projeto é facilitar o acesso a informações institucionais, documentos e dúvidas frequentes da universidade de forma automatizada, eficiente e interativa.

## 💡 Sobre o Projeto

O chatbot tem como propósito atender à comunidade acadêmica da UFABC (Universidade Federal do ABC), oferecendo respostas contextualmente relevantes a partir de uma base de documentos institucionais, como editais, regulamentos e informações acadêmicas.

A abordagem RAG combina técnicas de recuperação de documentos com geração de linguagem natural, permitindo que o chatbot consulte documentos reais antes de formular respostas, garantindo maior precisão e confiabilidade.

## ⚙️ Tecnologias e Conceitos

- **Retrieval-Augmented Generation (RAG)**
- **Processamento de Linguagem Natural (PLN)**

## 👥 Autores

- **Aline Milene Martins dos Santos**  
  📧 aline.milene@aluno.ufabc.edu.br  
  🔗 [github.com/AlineMilene](https://github.com/AlineMilene)

- **Leonardo Pires de Oliveira**  
  📧 oliveira.l@aluno.ufabc.edu.br  
  🔗 [github.com/LeonOliveir4](https://github.com/LeonOliveir4)

- **Matheus Victor Soares de Araujo**  
  📧 matheus.victor@aluno.ufabc.edu.br  
  🔗 [github.com/MatheusR42](https://github.com/MatheusR42)

---

Este projeto faz parte do Projeto de Graduação de Curso (PGC) na **Universidade Federal do ABC (UFABC)**.

## 🚀 Como executar o projeto localmente

1️⃣ Crie e ative um ambiente virtual (opcional, mas recomendado):

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate      # Windows
```

2️⃣ Instale as dependências:

```bash
pip install bm25s[full] fastapi uvicorn openai
uvicorn rag_pipeline.main:app --host 0.0.0.0 --port 8000 --reload
```

---

#### 🔹 Opção 1: vLLM (LLaMA 3.1)

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3.1-8B-Instruct
```

Configure o endpoint da LLM no arquivo `llama_client.py`:

```python
openai.base_url = "http://localhost:8000/v1"
```

##### 🔑 Acesso ao modelo LLaMA 3.1 (obrigatório)

1️⃣ Tenha uma conta no [Hugging Face](https://huggingface.co)  
2️⃣ Solicite acesso:  
👉 [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)  
3️⃣ Após aprovação, gere um Access Token em:  
👉 [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)  
4️⃣ Faça login local com o token:

```bash
pip install huggingface-hub
huggingface-cli login
```

#### ❗ Alternativa open-source:

```bash
python -m vllm.entrypoints.openai.api_server --model mistralai/Mistral-7B-Instruct-v0.2
```

---

#### 🔹 Opção 2: Ollama (mais leve)

1️⃣ Instale o Ollama:  
👉 [https://ollama.com/download](https://ollama.com/download)

2️⃣ Rode o modelo desejado (exemplo com LLaMA 3):

```bash
ollama run llama3:8b
# ou outro modelo:
ollama run mistral
```

3️⃣ Configure o endpoint no `llama_client.py`:

```python
openai.api_key = "sk-no-key-needed"
openai.base_url = "http://localhost:11434/v1"
```

4️⃣ Execute o servidor FastAPI normalmente:

```bash
uvicorn rag_pipeline.main:app --host 0.0.0.0 --port 8000 --reload
```

5️⃣ Acesse a interface de testes:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

📚 Modelos suportados por Ollama (exemplos):

- `llama3:8b`
- `mistral`
- `codellama`
- `phi3`
- `gemma`

Veja mais em: [https://ollama.com/library](https://ollama.com/library)

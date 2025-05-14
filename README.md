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

3️⃣ Para uso com LLaMA local (vLLM)

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server --model meta-llama/Meta-Llama-3-8B-Instruct
```
#### Configure o endpoint da LLM no arquivo llama_client.py para:
```bash
openai.base_url = "http://localhost:8000/v1"
```

### 🔑 Acesso ao modelo LLaMA 3.1 (obrigatório)

Para usar o modelo `meta-llama/Llama-3.1-8B-Instruct` com vLLM, você precisa:

1️⃣ Ter uma conta no [Hugging Face](https://huggingface.co)

2️⃣ Solicitar acesso ao modelo na página:  
[https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)

3️⃣ Após aprovação (leva de 1 a 5 dias), gerar um Access Token em:  
[https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)  
👉 Selecione permissão `Read` ao criar o token.

4️⃣ Logar na sua máquina usando o token:
```bash
pip install huggingface-hub
huggingface-cli login
```

### ❗ Importante: se desejar testar o pipeline antes da aprovação, utilize o modelo open-source:

```bash
python -m vllm.entrypoints.openai.api_server --model mistralai/Mistral-7B-Instruct-v0.2
```
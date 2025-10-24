# 🤖 Chatbot Assistente UFABC (RAG)

Chatbot para a UFABC baseado em **Retrieval-Augmented Generation (RAG)**. Ele busca trechos em documentos institucionais (PDFs, tabelas e imagens), sumariza e usa um LLM para responder com contexto.

## ✨ Principais features

- **RAG multimodal**: texto, tabelas (HTML) e imagens (sumarizadas na indexação)
- **Persistência**: vetores em **Chroma** e **docstore** em disco (LocalFileStore)
- **Reidratação inteligente**: se o docstore sumir, ele é reconstruído **sem re-embedar**
- **API FastAPI** (concorrência pronta) + **CLI** (modo terminal)
- **Ollama** para embeddings locais (fallbacks de LLM: Groq/OpenAI, se configurados)
- **Classificação robusta** em `parse_docs` (evita confundir texto com base64)

## 🗂️ Estrutura do projeto

```
rag_pipeline/
├── __init__.py
├── api.py                     # FastAPI (serviço)
├── main.py                    # CLI (terminal)
├── config.py                  # Paths absolutos e configs
├── core/
│   ├── models.py              # get_llama_model / get_llava_model
│   ├── prompt_utils.py        # parse_docs, build_prompt etc.
│   └── retriever_pipeline.py  # get_rag_pipeline (Opção B com reidratação)
├── data/
│   ├── pdf_utils.py           # extração (unstructured) e classificação
│   ├── summarization.py       # sumarização + add_documents (vectorstore + docstore)
│   └── retry.py               # retry_with_backoff
├── utils/
│   ├── display_utils.py       # helper p/ exibir imagens base64 (CLI)
│   └── ...
└── .cache_chunks/             # gerado em runtime (chroma_store, summaries, chunks)
```

## 🧩 Requisitos

- Python **3.10+**
- [Ollama](https://ollama.com/download) (para embeddings locais)
- (Opcional) chaves **OpenAI** / **Groq** para fallback do LLM

### Instalação

1. **Clone o repositório e configure o ambiente Python**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate     # Linux/macOS
   # .venv\Scripts\activate      # Windows
   
   cd rag_pipeline

   pip install -r requirements.txt
   ```

2. **Configure as variáveis de ambiente**:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas chaves de API
   ```

3. **Verifique se o Ollama está rodando**:
   ```bash
   ollama serve
   ```

4. **Se for usar modelos locais, instale os modelos**:
   ```bash
   ollama pull llama3.2:latest
   ollama pull nomic-embed-text:latest
   ```

> **Nota**: Se o `unstructured.partition.pdf` pedir extras (OCR), instale variantes como `unstructured[all-docs]`.

## 🔐 Configuração de Variáveis de Ambiente

### Setup para Desenvolvimento

1. **Copie o arquivo de exemplo**:
   ```bash
   cp .env.example .env
   ```

2. **Edite o arquivo `.env`** com suas chaves reais:
   ```bash
   # API Keys obrigatórias
   GROQ_API_KEY=sua_chave_groq_aqui
   OPENAI_API_KEY=sua_chave_openai_aqui
   
   # Base URL do Ollama (padrão: localhost)
   OLLAMA_BASE_URL=http://localhost:11434
   
   # Provedor de modelo para geração de texto (padrão: ollama)
   # Opções: ollama, openai, groq
   MODEL_PROVIDER=ollama
   ```

### Obtendo as API Keys

- **Groq**: Registre-se em [console.groq.com](https://console.groq.com) para obter sua chave gratuita
- **OpenAI**: Acesse [platform.openai.com/api-keys](https://platform.openai.com/api-keys) para gerar uma API key

### Configuração para Produção/Servidor

Em ambiente de produção, defina as variáveis de ambiente diretamente no sistema:

```bash
# Linux/macOS
export GROQ_API_KEY="sua_chave_groq"
export OPENAI_API_KEY="sua_chave_openai"
export OLLAMA_BASE_URL="http://seu-servidor-ollama:11434"
export MODEL_PROVIDER="ollama"

# Windows
set GROQ_API_KEY=sua_chave_groq
set OPENAI_API_KEY=sua_chave_openai
set OLLAMA_BASE_URL=http://seu-servidor-ollama:11434
set MODEL_PROVIDER=ollama
```

### Validação das Variáveis

O sistema valida automaticamente se todas as variáveis obrigatórias estão configuradas:
- `GROQ_API_KEY`
- `OPENAI_API_KEY` 
- `OLLAMA_BASE_URL`
- `MODEL_PROVIDER` (opcional, padrão: "ollama")

Se alguma variável estiver faltando, você verá um erro como:
```
ValueError: Missing required environment variables: GROQ_API_KEY, OLLAMA_BASE_URL
```

## 📦 Baixar os modelos no Ollama

Certifique-se de que o Ollama está rodando (ollama serve) e então baixe os modelos usados pelo projeto:
```bash
# LLM para geração de respostas
ollama pull llama3.1:8b

# LLM multimodal para sumarizar imagens na indexação
ollama pull llava:13b

# Modelo de embeddings (texto)
ollama pull nomic-embed-text

# Certifica que os modelos estão instalados
ollama list
```

No **Windows**, para expor o Ollama para a rede/WSL:

```powershell
$env:OLLAMA_HOST="0.0.0.0:11434"
$env:OLLAMA_ORIGINS="*"
ollama serve
# libere a porta 11434 no Firewall do Windows
```


Comando para iniciar a API:

```
uvicorn api:app --reload
```

Como fazer perguntas:

Pergunta unica:
```
curl --request POST \
  --url http://127.0.0.1:8000/ask \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.5.0' \
  --data '{
	"question": "quantas vezes posso trancar a matricula?"
}'
```

Modo Chat:
```
curl --request POST \
  --url http://127.0.0.1:8000/chat \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/11.5.0' \
  --data '{
	"messages": [
	{"role": "user", "content": "Me explique brevemente sobre a matricula"},	
			{"role": "system", "content": "Olá!"},
{"role": "user", "content": "Olá"}
	]
}'
```

## 🗺️ Configuração de paths

Os paths são absolutos (via `Path.resolve()`) a partir da raiz do repositório:

- PDFs: `data_extraction/documentos_ufabc/Prograd`
- Cache de chunks: `.cache_chunks/chunks_classificados.json`
- Cache de summaries: `.cache_chunks/summaries.json`
- Vetores/Chroma + docstore: `.cache_chunks/chroma_store/`

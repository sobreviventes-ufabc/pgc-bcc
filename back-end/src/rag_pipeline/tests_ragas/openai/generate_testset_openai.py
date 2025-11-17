"""
Versão aprimorada da geração de testset RAGAS com OpenAI
Gera CSV compatível com RAGAS, incluindo colunas:
question, answer, ground_truth, contexts

Uso:
  1. Configure sua chave:  set OPENAI_API_KEY=sua_chave_aqui
  2. Coloque os PDFs em:   data_extraction/documentos_ufabc/
  3. Rode:                python generate_testset.py
"""

import os
import time
import logging
import pandas as pd
from glob import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage

# ============================================================
# Configurações gerais
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_DIR = os.path.join(BASE_DIR, "data_extraction", "documentos_ufabc")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "testset.csv")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("❌ Variável OPENAI_API_KEY não encontrada. Defina antes de executar.")

MODEL_NAME = "gpt-4o-mini"
TEST_SIZE = 50       # número de amostras a gerar
DELAY = 1.5         # segundos entre chamadas (para evitar rate limit)
CHUNK_SIZE = 800    # tamanho máximo dos contextos
CHUNK_OVERLAP = 100

# ============================================================
# Inicializa modelo OpenAI
# ============================================================
def make_llm():
    log.info(f"🚀 Inicializando modelo OpenAI: {MODEL_NAME}")
    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=0.7,
        api_key=OPENAI_API_KEY,
        max_retries=2,
        timeout=60,
    )

llm = make_llm()

# ============================================================
# Leitura e divisão dos PDFs
# ============================================================
def load_docs():
    pdfs = glob(os.path.join(DOCS_DIR, "**", "*.pdf"), recursive=True)
    docs = []
    for pdf in pdfs:
        loader = PyPDFLoader(pdf)
        loaded = loader.load()
        docs.extend(loaded)
        log.info("📄 Carregado: %s (%d páginas)", os.path.basename(pdf), len(loaded))
    return docs

def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    splits = splitter.split_documents(docs)
    log.info("🧩 Gerados %d chunks (~%d caracteres cada)", len(splits), CHUNK_SIZE)
    return splits

# ============================================================
# Geração de pergunta e resposta
# ============================================================
def generate_question(context):
    """Gera uma pergunta curta e direta baseada no contexto."""
    prompt = f"""
Gere uma única pergunta objetiva e curta baseada no texto abaixo.
A pergunta deve ser clara e possível de responder usando apenas este texto.

Texto:
{context[:1000]}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip().replace("\n", " ")
    except Exception as e:
        log.warning("Erro ao gerar pergunta: %s", e)
        return None

def generate_answer(context, question):
    """Gera uma resposta direta e fiel ao contexto."""
    prompt = f"""
Responda de forma **natural, completa e direta** à pergunta a seguir,
usando **somente as informações presentes no texto abaixo**.
Reescreva a resposta em uma frase gramaticalmente correta,
mas **sem adicionar interpretações ou informações novas**
Certifique-se de **incluir todos os detalhes relevantes** (como datas, horários e condições).

Texto:
{context[:1000]}

Pergunta:
{question}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip().replace("\n", " ")
    except Exception as e:
        log.warning("Erro ao gerar resposta: %s", e)
        return None

# ============================================================
# Função principal
# ============================================================
def main():
    log.info("📂 Lendo documentos da pasta: %s", DOCS_DIR)
    docs = load_docs()
    if not docs:
        raise RuntimeError("❌ Nenhum PDF encontrado em data_extraction/documentos_ufabc/")

    splits = split_docs(docs)
    samples = splits[:TEST_SIZE]
    results = []

    for i, doc in enumerate(samples):
        context = doc.page_content.strip()
        log.info("🧠 Gerando exemplo %d/%d...", i + 1, TEST_SIZE)

        q = generate_question(context)
        time.sleep(DELAY)
        a = generate_answer(context, q)
        time.sleep(DELAY)

        if not q or not a:
            log.warning("⚠️ Exemplo %d ignorado (falha na geração).", i + 1)
            continue

        # Contexto curto e limpo
        short_context = context[:800].replace("\n", " ").strip()
        results.append({
            "question": q,
            "answer": a,
            "ground_truth": a,
            "contexts": [context[i:i+700] for i in range(0, len(context), 700)][:3]
        })

    if not results:
        raise RuntimeError("❌ Nenhum exemplo foi gerado com sucesso.")

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    log.info("✅ Testset salvo com sucesso em: %s", OUTPUT_CSV)
    log.info("🧾 Colunas: %s", ", ".join(df.columns))
    log.info("📊 Total de exemplos gerados: %d", len(df))

# ============================================================
if __name__ == "__main__":
    main()
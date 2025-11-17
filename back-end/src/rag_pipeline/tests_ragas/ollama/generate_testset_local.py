"""
Versão aprimorada da geração de testset RAGAS com Ollama (rodando localmente)
Gera CSV compatível com RAGAS, incluindo colunas:
question, answer, ground_truth, contexts
"""

import os
import time
import logging
import pandas as pd
from glob import glob
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOllama
from langchain.schema import HumanMessage

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# Configurações
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS_DIR = os.path.join(BASE_DIR, "data_extraction", "documentos_ufabc")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "testset.csv")

# Modelo local do Ollama (certifique-se de que o servidor está rodando com `ollama serve`)
MODEL_NAME = "llama3"
TEST_SIZE = 5
DELAY = 2  # segundos entre chamadas

# Inicializa o modelo local do Ollama
try:
    llm = ChatOllama(model=MODEL_NAME, temperature=0.7)
except Exception as e:
    raise RuntimeError(f"Erro ao conectar ao Ollama. Certifique-se de que o servidor está ativo: {e}")

def load_docs():
    """Carrega os PDFs do diretório configurado."""
    pdfs = glob(os.path.join(DOCS_DIR, "**", "*.pdf"), recursive=True)
    docs = []
    for pdf in pdfs:
        loader = PyPDFLoader(pdf)
        loaded = loader.load()
        docs.extend(loaded)
        log.info("Carregado: %s (%d páginas)", os.path.basename(pdf), len(loaded))
    return docs

def split_docs(docs):
    """Divide os documentos em chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    splits = splitter.split_documents(docs)
    log.info("Gerados %d chunks", len(splits))
    return splits

def generate_question(context):
    """Gera uma pergunta relevante para um chunk usando o modelo local."""
    prompt = f"""
Você é um gerador de perguntas curtas e diretas baseadas em texto.
Gere **apenas** uma pergunta objetiva sobre o conteúdo abaixo.
Não adicione prefixos como 'Pergunta:' ou explicações.

Texto base:
{context[:1000]}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])  # usa invoke() em vez de __call__
        return response.content.strip()
    except Exception as e:
        log.warning("Erro ao gerar pergunta: %s", e)
        return None

def generate_answer(context, question):
    """Gera uma resposta objetiva e direta para a pergunta."""
    prompt = f"""
Responda de forma direta à pergunta a seguir com base **exclusivamente** no texto.
Não inclua prefixos como 'Resposta:' nem frases explicativas.

Texto:
{context[:1000]}

Pergunta:
{question}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        log.warning("Erro ao gerar resposta: %s", e)
        return None

def main():
    docs = load_docs()
    splits = split_docs(docs)
    samples = splits[:TEST_SIZE]

    results = []
    for i, doc in enumerate(samples):
        context = doc.page_content
        log.info("Gerando exemplo %d/%d...", i + 1, TEST_SIZE)

        q = generate_question(context)
        time.sleep(DELAY)
        a = generate_answer(context, q)
        time.sleep(DELAY)

        if not q or not a:
            log.warning("Exemplo %d ignorado (falha na geração).", i + 1)
            continue

        results.append({
            "question": q,
            "answer": a,
            "ground_truth": a,              # ground_truth = resposta ideal
            "contexts": [context[:300] + "..."]  # lista de contextos (para o RAGAS)
        })

    if not results:
        raise RuntimeError("Nenhum exemplo foi gerado. Verifique o modelo e os documentos.")

    df = pd.DataFrame(results)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    log.info("✅ Testset salvo com sucesso em %s", OUTPUT_CSV)
    log.info("Colunas do CSV: %s", ", ".join(df.columns))

if __name__ == "__main__":
    main()

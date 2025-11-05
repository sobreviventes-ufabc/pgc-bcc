"""
evaluate_ragas_local.py
Versão 100% local (sem timeout) para avaliação RAGAS usando modelo Ollama (llama3).
Executa métricas: faithfulness, answer_relevancy, context_precision, context_recall.
"""

import os
import logging
import ast
import time
import pandas as pd
from datasets import Dataset

# === Configuração global do RAGAS ===
import ragas
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from langchain_ollama import OllamaEmbeddings


# Força execução totalmente sequencial (sem threads/async)
ragas.CONCURRENCY_LIMIT = 1
ragas.USE_MULTIPROCESSING = False

# === Configuração de logs ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# === Caminhos ===
TESTSET_CSV = os.path.join(os.path.dirname(__file__), "testset.csv")
OUT_EVAL_CSV = os.path.join(os.path.dirname(__file__), "eval.csv")
OUT_SUMMARY = os.path.join(os.path.dirname(__file__), "metrics_summary.txt")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")


# === Inicializa LLM local (Ollama) ===
try:
    from langchain_ollama import ChatOllama
except ImportError:
    raise ImportError(
        "❌ Pacote 'langchain-ollama' não encontrado.\n"
        "Instale com: pip install langchain-ollama"
    )

def make_llm():
    log.info("🚀 Inicializando modelo local 'phi3:mini' com Ollama...")
    try:
        llm_instance = ChatOllama(
            model="llama3.1:8b",
            base_url=OLLAMA_BASE_URL,
            temperature=0,
            num_ctx=32900,
            num_predict=512,
            verbose=False,
            timeout=None
        )
        log.info("✅ LLM local 'llama3.1:8b' inicializado com sucesso.")
        return llm_instance
    except Exception as e:
        raise RuntimeError(f"Falha ao inicializar LLM local via Ollama: {e}")

llm = make_llm()

# === Função para carregar o dataset ===
def load_testset(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"❌ Testset CSV não encontrado: {csv_path}. "
            "Rode generate_testset.py primeiro."
        )

    df = pd.read_csv(csv_path)

    rename_map = {"reference": "ground_truth", "retrieved_contexts": "contexts"}
    df.rename(columns=rename_map, inplace=True)

    if "contexts" not in df.columns:
        log.warning("Coluna 'contexts' ausente — criando lista vazia para cada linha.")
        df["contexts"] = [[] for _ in range(len(df))]

    def _to_list(x):
        if pd.isna(x):
            return []
        if isinstance(x, list):
            return x
        try:
            return ast.literal_eval(x)
        except Exception:
            return [str(x)]

    df["contexts"] = df["contexts"].apply(_to_list)

    for col in ["question", "answer"]:
        if col not in df.columns:
            raise ValueError(f"O CSV deve conter a coluna '{col}'.")

    if "ground_truth" not in df.columns:
        log.warning("Coluna 'ground_truth' ausente. Usando 'answer' como ground_truth.")
        df["ground_truth"] = df["answer"]

    return df

# === Avaliação robusta (sem timeout, com retry local) ===
def safe_evaluate(dataset, metrics, llm, retries=3, delay=10):
    for attempt in range(1, retries + 1):
        try:
            log.info(f"🧠 Execução tentativa {attempt}/{retries}")

            # ✅ Força embeddings locais via Ollama
            embeddings = OllamaEmbeddings(
                model="nomic-embed-text",
                base_url=OLLAMA_BASE_URL
            )

            return evaluate(dataset=dataset, metrics=metrics, llm=llm, embeddings=embeddings)

        except Exception as e:
            log.error(f"Erro na tentativa {attempt}: {e}")
            if attempt < retries:
                log.info(f"⏳ Aguardando {delay} segundos antes de tentar novamente...")
                time.sleep(delay)
            else:
                raise

# === Função principal ===
def main():
    log.info("📂 Lendo testset: %s", TESTSET_CSV)
    df = load_testset(TESTSET_CSV)
    dataset = Dataset.from_dict(df.to_dict(orient="list"))
    log.info("✅ Dataset pronto para avaliação com %d amostras", len(dataset))

    metrics = [answer_relevancy]
    if df["contexts"].apply(len).any():
        metrics += [faithfulness, context_precision, context_recall]
    log.info("📊 Métricas a calcular: %s", [m.name for m in metrics])

    # === Execução da avaliação (sem limite de tempo) ===
    log.info("🧠 Iniciando avaliação com modelo local (sem limite de tempo)...")
    results = safe_evaluate(dataset, metrics, llm)
    log.info("✅ Avaliação concluída.")

    # === Salva resultados ===
    try:
        df_results = results.to_pandas()
        df_results.to_csv(OUT_EVAL_CSV, index=False)
        log.info("💾 Resultados por amostra salvos em %s", OUT_EVAL_CSV)
    except Exception as e:
        log.error("Falha ao salvar resultados: %s", e)
        return

    # === Gera resumo ===
    try:
        numeric_cols = df_results.select_dtypes(include=["float64", "int64"]).columns
        summary_dict = {col: df_results[col].mean() for col in numeric_cols}
        with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
            f.write("Resumo da Avaliação RAGAS\n")
            f.write("==========================\n\n")
            for k, v in summary_dict.items():
                f.write(f"{k}: {v:.4f}\n")
        log.info("📈 Resumo salvo em %s", OUT_SUMMARY)
    except Exception as e:
        log.warning("Não foi possível gerar resumo: %s", e)

if __name__ == "__main__":
    main()

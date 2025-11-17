"""
evaluate_ragas_openai.py
Versão corrigida e otimizada para avaliação de testsets RAG usando RAGAS + OpenAI.
Executa métricas: faithfulness, answer_relevancy, context_precision, context_recall.
Compatível com GPT-4o-mini (baixo custo) ou GPT-4o (melhor qualidade).
"""

import os
import logging
import ast
import json
import time
import pandas as pd
from datasets import Dataset

# === Dependências principais ===
import ragas
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# === Configurações globais ===
ragas.CONCURRENCY_LIMIT = 1
ragas.USE_MULTIPROCESSING = False

# === Logs ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# === Caminhos ===
BASE_DIR = os.path.dirname(__file__)
TESTSET_CSV = os.path.join(BASE_DIR, "testset.csv")
OUT_EVAL_CSV = os.path.join(BASE_DIR, "eval.csv")
OUT_SUMMARY = os.path.join(BASE_DIR, "metrics_summary.txt")

# === Chave da API ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError(
        "❌ Variável de ambiente OPENAI_API_KEY não encontrada.\n"
        "Defina com: set OPENAI_API_KEY=sua_chave_aqui"
    )

# === Inicializa modelo ===
def make_llm(model_name="gpt-4o-mini"):
    log.info(f"🚀 Inicializando modelo OpenAI {model_name}...")
    llm_instance = ChatOpenAI(
        model=model_name,
        temperature=0,
        api_key=OPENAI_API_KEY,
        max_retries=2,
        timeout=60,
    )
    log.info("✅ Modelo inicializado com sucesso.")
    return llm_instance

llm = make_llm("gpt-4o-mini")  # troque para "gpt-4o" se quiser mais precisão


# === Função segura para parse de contextos ===
def safe_parse_contexts(x):
    if pd.isna(x):
        return []
    if isinstance(x, list):
        return x
    # Tenta converter string de lista Python → lista real
    try:
        val = ast.literal_eval(x)
        if isinstance(val, list):
            return val
        return [str(val)]
    except Exception:
        # Tenta JSON como fallback
        try:
            return json.loads(x.replace("'", '"'))
        except Exception:
            # Fallback: trata como lista de 1 item
            return [x]


# === Limpeza de texto (remove \n, espaços etc.) ===
def clean_text_list(lst):
    if not isinstance(lst, list):
        return []
    return [str(c).replace("\\n", " ").replace("\n", " ").strip() for c in lst]


# === Carrega o testset ===
def load_testset(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"❌ Testset CSV não encontrado: {csv_path}")

    df = pd.read_csv(csv_path)
    rename_map = {"reference": "ground_truth", "retrieved_contexts": "contexts"}
    df.rename(columns=rename_map, inplace=True)

    required = ["question", "answer"]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"O CSV deve conter a coluna '{col}'.")

    if "ground_truth" not in df.columns:
        df["ground_truth"] = df["answer"]

    if "contexts" not in df.columns:
        df["contexts"] = [[] for _ in range(len(df))]

    df["contexts"] = df["contexts"].apply(safe_parse_contexts).apply(clean_text_list)

    # Normaliza campos principais
    for col in ["question", "answer", "ground_truth"]:
        df[col] = df[col].astype(str).str.strip().str.replace("\\n", " ").str.replace("\n", " ")

    log.info("✅ Testset carregado e normalizado (%d amostras).", len(df))
    return df


# === Avaliação com retry ===
def safe_evaluate(dataset, metrics, llm, retries=3, delay=10):
    for attempt in range(1, retries + 1):
        try:
            log.info(f"🧠 Tentativa {attempt}/{retries} de avaliação...")
            embeddings = OpenAIEmbeddings(
                model="text-embedding-3-small",
                api_key=OPENAI_API_KEY,
            )
            results = evaluate(dataset=dataset, metrics=metrics, llm=llm, embeddings=embeddings)
            return results
        except Exception as e:
            log.error(f"Erro na tentativa {attempt}: {e}")
            if attempt < retries:
                log.info(f"⏳ Aguardando {delay}s antes de tentar novamente...")
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
    log.info("📊 Métricas selecionadas: %s", [m.name for m in metrics])

    # print(df["contexts"].iloc[0])
    # print(type(df["contexts"].iloc[0]))

    log.info("🧠 Iniciando avaliação via OpenAI...")
    results = safe_evaluate(dataset, metrics, llm)
    log.info("✅ Avaliação concluída.")

    df_results = results.to_pandas()
    df_results.to_csv(OUT_EVAL_CSV, index=False)
    log.info("💾 Resultados detalhados salvos em %s", OUT_EVAL_CSV)

    # === Resumo das métricas ===
    numeric_cols = df_results.select_dtypes(include=["float64", "int64"]).columns
    summary = {col: df_results[col].mean() for col in numeric_cols}

    with open(OUT_SUMMARY, "w", encoding="utf-8") as f:
        f.write("Resumo da Avaliação RAGAS\n")
        f.write("==========================\n\n")
        for k, v in summary.items():
            f.write(f"{k}: {v:.4f}\n")

    log.info("📈 Resumo salvo em %s", OUT_SUMMARY)
    for k, v in summary.items():
        log.info("%s: %.4f", k, v)


if __name__ == "__main__":
    main()
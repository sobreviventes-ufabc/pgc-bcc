import json
from pathlib import Path
import shutil

from langchain_community.vectorstores import Chroma
from langchain_ollama.embeddings import OllamaEmbeddings
from langchain.storage import LocalFileStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from config import PDF_DIR, CHUNKS_PATH, SUMMARIES_PATH, PERSIST_DIR
from core.models import get_llama_model
from data.pdf_utils import extract_chunks_from_pdf, classify_chunks
from data.summarization import summarize_elements, summarize_images, add_documents
from core.prompt_utils import parse_docs, build_prompt, clean_summary


def _docstore_is_empty(docstore_dir: Path) -> bool:
    try:
        next(docstore_dir.iterdir())
        return False
    except StopIteration:
        return True
    except FileNotFoundError:
        return True


def _rehydrate_docstore_only(retriever: MultiVectorRetriever, all_texts, all_tables, all_images):
    """Rehidrata SOMENTE o docstore com os ORIGINAIS, sem re-embedar.
    Mantém a MESMA ordem de indexação: textos -> tabelas -> imagens.
    """
    # Recupera os doc_ids que já estão no Chroma (na mesma ordem em que foram inseridos)
    meta = retriever.vectorstore.get(include=["metadatas"]).get("metadatas", [])
    doc_ids = [m.get("doc_id") for m in meta]

    # Concatena os originais na mesma ordem usada no indexing inicial
    all_originals = list(all_texts) + list(all_tables) + list(all_images)

    if len(all_originals) != len(doc_ids):
        print(f"[rehydrate] Aviso: contagem não bate (originais={len(all_originals)} vs doc_ids={len(doc_ids)}).")
        # Em caso de divergência, tenta limitar ao mínimo comum:
        n = min(len(all_originals), len(doc_ids))
        all_originals = all_originals[:n]
        doc_ids = doc_ids[:n]

    # Grava em bytes no docstore
    pairs = []
    for i, orig in enumerate(all_originals):
        if isinstance(orig, str):
            pairs.append((doc_ids[i], orig.encode("utf-8")))
        else:
            pairs.append((doc_ids[i], orig))
    retriever.docstore.mset(pairs)
    print(f"[rehydrate] Docstore reidratado com {len(pairs)} itens.")


# --- FUNÇÃO PRINCIPAL DE INICIALIZAÇÃO DA PIPELINE (Opção B) ---
def get_rag_pipeline(force_regenerate=False):
    """
    Inicializa o retriever e a pipeline RAG.
    - Se force_regenerate=True ou não há vetores: refaz chunks, summaries, embeddings e docstore.
    - Senão: se docstore está vazio, rehidrata só o docstore (sem re-embedar).
    """
    # 1) Carrega/gera chunks (originais)
    if not CHUNKS_PATH.exists() or force_regenerate:
        pdf_files = list(PDF_DIR.rglob("*.pdf"))
        print(f"{len(pdf_files)} arquivos PDF encontrados.")

        all_texts, all_tables, all_images = [], [], []
        for pdf in pdf_files:
            chunks = extract_chunks_from_pdf(pdf)
            texts, tables, images = classify_chunks(chunks)
            all_texts.extend(texts)
            all_tables.extend(tables)
            all_images.extend(images)
        
        if force_regenerate and PERSIST_DIR.exists():
            shutil.rmtree(PERSIST_DIR)
            print("[force_regenerate] Limpando diretório persistente...")

        with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump({"texts": all_texts, "tables": all_tables, "images": all_images}, f, ensure_ascii=False, indent=2)
    else:
        print("Usando cache de chunks existente.")
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        all_texts = data["texts"]
        all_tables = data["tables"]
        all_images = data["images"]

    print(f"\nTextos: {len(all_texts)}, Tabelas: {len(all_tables)}, Imagens: {len(all_images)}")

    # 2) Vectorstore + docstore (persistidos)
    embedding_functions = OllamaEmbeddings(model="nomic-embed-text", base_url="http://192.168.18.9:11434")
    vectorstore = Chroma(
        collection_name="multi_modal_rag",
        embedding_function=embedding_functions,
        persist_directory=str(PERSIST_DIR)
    )
    docstore_dir = PERSIST_DIR / "docstore"
    docstore_dir.mkdir(parents=True, exist_ok=True)
    store = LocalFileStore(str(docstore_dir))
    retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=store, id_key="doc_id", search_kwargs={"k": 20})

    vector_ids = vectorstore.get().get("ids", [])
    has_vectors = len(vector_ids) > 0
    docstore_empty = _docstore_is_empty(docstore_dir)

    # 3) Fluxos
    if force_regenerate or not has_vectors:
        print("\n[regen] Resumindo os elementos extraídos...")
        text_summaries = summarize_elements(all_texts)
        table_summaries = summarize_elements(all_tables, is_table=True)
        image_summaries = summarize_images(all_images) if all_images else []

        with open(SUMMARIES_PATH, "w", encoding="utf-8") as f:
            json.dump({
                "text_summaries": text_summaries,
                "table_summaries": table_summaries,
                "image_summaries": image_summaries
            }, f, ensure_ascii=False, indent=2)

        # Indexa vetores e popula docstore numa tacada só
        add_documents(all_texts, text_summaries, retriever)
        add_documents(all_tables, table_summaries, retriever)
        add_documents(all_images, image_summaries, retriever)

        print("[regen] Embeddings, summaries e docstore gerados do zero.")
    else:
        print("\nVetores indexados:", len(vector_ids))
        if docstore_empty:
            print("[rehydrate] Vetores existem, mas docstore está vazio. Rehidratando...")
            # Precisamos apenas dos ORIGINAIS (CHUNKS_PATH). Summaries não são necessários aqui.
            _rehydrate_docstore_only(retriever, all_texts, all_tables, all_images)
        else:
            print("\nUsando embeddings e documentos previamente gerados.")

    # 4) Monta a chain
    model = get_llama_model()
    chain_with_sources = (
        {"context": retriever | RunnableLambda(parse_docs), "question": RunnablePassthrough()}
        | RunnablePassthrough().assign(
            response=(RunnableLambda(build_prompt) | model | StrOutputParser())
        )
    )
    return chain_with_sources
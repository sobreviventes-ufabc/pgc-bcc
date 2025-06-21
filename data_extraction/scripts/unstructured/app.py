import os
import json
import time
import base64
import uuid
import random

from pathlib import Path
from base64 import b64decode
from IPython.display import Image, display
from unstructured.partition.pdf import partition_pdf
from concurrent.futures import ThreadPoolExecutor, as_completed

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage

from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.schema.document import Document
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.retrievers.multi_vector import MultiVectorRetriever

# CONFIG
os.environ["GROQ_API_KEY"] = "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" 
os.environ["OPENAI_API_KEY"] = "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"
PDF_DIR = Path(r"C:\Users\User\Desktop\code\pgc-bcc\data_extraction\documentos_ufabc\Prograd\Sobre\Apresentacoes")
OLLAMA_MODEL = "llama3"
CHUNKS_PATH = Path(".cache_chunks/chunks_classificados.json")
CHUNKS_PATH.parent.mkdir(parents=True, exist_ok=True)
MAX_WORKERS = min(10, os.cpu_count() or 4)

# ----------------- Modelo com fallback + log -------------------
def get_chat_model():
    try:
        model = ChatOllama(model=OLLAMA_MODEL)
        print(f"🔧 Usando modelo local: Ollama - {OLLAMA_MODEL}")
        return model
    except Exception:
        try:
            model = ChatGroq(model="llama3-8b-8192")
            print("🔧 Usando modelo via Groq: llama3-8b-8192")
            return model
        except Exception:
            model = ChatOpenAI(model="gpt-4o-mini")
            print("🔧 Usando modelo via OpenAI: gpt-4o-mini")
            return model

# ---------------- Retry ----------------
def retry_with_backoff(fn, retries=5, base_delay=5, max_delay=60):
    for attempt in range(retries):
        try:
            return fn()
        except Exception as e:
            if "rate limit" in str(e).lower() or "429" in str(e):
                wait = min(max_delay, base_delay * 2 ** attempt + random.uniform(0, 1))
                print(f"⏳ Rate limit excedido. Retentando em {wait:.1f}s... ({attempt+1})")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("❌ Máximo de tentativas atingido.")

# ------------- PDF e classificação --------------
def extract_chunks_from_pdf(file_path: Path):
    try:
        start_time = time.time()
        chunks = partition_pdf(
            filename=str(file_path),
            infer_table_structure=True,
            strategy="hi_res",
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            chunking_strategy="by_title",
            max_characters=10000,
            combine_text_under_n_chars=2000,
            new_after_n_chars=6000,
        )
        duration = time.time() - start_time
        print(f"✅ {file_path.name}: {len(chunks)} chunks extraídos em {duration:.2f}s")
        return chunks
    except Exception as e:
        print(f"❌ Erro ao processar {file_path.name}: {e}")
        return []

def classify_chunks(chunks):
    texts, tables, images = [], [], []
    for chunk in chunks:
        if "Table" in str(type(chunk)):
            tables.append(chunk.metadata.text_as_html)
        if "CompositeElement" in str(type(chunk)):
            texts.append(chunk.text)
            for el in chunk.metadata.orig_elements:
                if "Image" in str(type(el)):
                    images.append(el.metadata.image_base64)
    return texts, tables, images

# --------- RESUMO COM MODELO + Retry (1 por vez) ---------
def summarize_elements(elements, is_table=False):
    prompt_template = """
    Você é um assistente encarregado de resumir tabelas e textos.
    Apresente um resumo conciso da tabela ou texto.
    Responda apenas com o resumo, sem comentários adicionais.
    Tabela ou trecho de texto: {element}
    """
    model = get_chat_model()
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

    summaries = []

    def summarize_single(element):
        return retry_with_backoff(lambda: chain.invoke({"element": element}))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_element = {executor.submit(summarize_single, el): el for el in elements}
        for future in as_completed(future_to_element):
            try:
                summaries.append(future.result())
            except Exception as e:
                print(f"⚠️ Erro ao resumir elemento: {e}")
                summaries.append("Erro ao resumir.")

    return summaries

# ----------- Imagens ---------------
def summarize_images(images):
    prompt_text = "Describe the image in detail. The image is part of a scientific paper on transformer architectures."
    model = get_chat_model()
    summaries = []

    def summarize_image(img_b64):
        prompt = ChatPromptTemplate.from_messages([HumanMessage(content=[
            {"type": "text", "text": prompt_text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
        ])])
        chain = prompt | model | StrOutputParser()
        return retry_with_backoff(lambda: chain.invoke({}))

    with ThreadPoolExecutor() as executor:
        future_to_image = {executor.submit(summarize_image, img): img for img in images}
        for future in as_completed(future_to_image):
            try:
                summaries.append(future.result())
            except Exception as e:
                print(f"⚠️ Erro ao resumir imagem: {e}")
                summaries.append("Erro ao resumir imagem.")

    return summaries

def display_base64_image(base64_code):
    image_data = base64.b64decode(base64_code)
    display(Image(data=image_data))

# ----------- Pipeline principal RAG multimodal -----------
def parse_docs(docs):
    b64, text = [], []
    for doc in docs:
        try:
            b64decode(doc)
            b64.append(doc)
        except:
            text.append(doc)
    return {"images": b64, "texts": text}

def build_prompt(kwargs):
    docs = kwargs["context"]
    question = kwargs["question"]
    context_text = "".join(docs["texts"])
    prompt_content = [
        {"type": "text", "text": f"""
        Responda à pergunta usando apenas o seguinte contexto. O contexto pode conter texto, tabelas e referências a imagens.

        Contexto: {context_text}
        Pergunta: {question}
        """}
    ]
    for image in docs["images"]:
        prompt_content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image}"}})
    return ChatPromptTemplate.from_messages([HumanMessage(content=prompt_content)])

def main():
    regenerate = input("🔄 Deseja gerar os chunks novamente? (s/n): ").strip().lower() == "s"

    if not CHUNKS_PATH.exists() or regenerate:
        pdf_files = list(PDF_DIR.rglob("*.pdf"))
        print(f"📄 {len(pdf_files)} arquivos PDF encontrados.")

        all_texts, all_tables, all_images = [], [], []
        for pdf in pdf_files:
            chunks = extract_chunks_from_pdf(pdf)
            texts, tables, images = classify_chunks(chunks)
            all_texts.extend(texts)
            all_tables.extend(tables)
            all_images.extend(images)

        with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
            json.dump({"texts": all_texts, "tables": all_tables, "images": all_images}, f, indent=2)

    else:
        print("✅ Usando cache existente.")
        with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_texts = data["texts"]
            all_tables = data["tables"]
            all_images = data["images"]

    print(f"\n📝 Textos: {len(all_texts)}, 📊 Tabelas: {len(all_tables)}, 🖼️ Imagens: {len(all_images)}")
    print("\n⏳ Resumindo os elementos extraídos...")

    text_summaries = summarize_elements(all_texts)
    table_summaries = summarize_elements(all_tables, is_table=True)
    image_summaries = summarize_images(all_images) if all_images else []

    vectorstore = Chroma(collection_name="multi_modal_rag", embedding_function=OpenAIEmbeddings())
    store = InMemoryStore()
    retriever = MultiVectorRetriever(vectorstore=vectorstore, docstore=store, id_key="doc_id")

    def add_documents(originals, summaries):
        ids = [str(uuid.uuid4()) for _ in originals]
        retriever.vectorstore.add_documents([
            Document(page_content=s, metadata={"doc_id": ids[i]}) for i, s in enumerate(summaries)
        ])
        retriever.docstore.mset(list(zip(ids, originals)))

    add_documents(all_texts, text_summaries)
    add_documents(all_tables, table_summaries)
    add_documents(all_images, image_summaries)

    chain_with_sources = {
        "context": retriever | RunnableLambda(parse_docs),
        "question": RunnablePassthrough(),
    } | RunnablePassthrough().assign(
        response=(RunnableLambda(build_prompt) | get_chat_model() | StrOutputParser())
    )

    while True:
        user_input = input("\n❓ Pergunta (ou 'sair'): ")
        if user_input.strip().lower() == "sair":
            break

        print("\n🔎 Buscando resposta...")
        response = chain_with_sources.invoke(user_input)
        print("\n🧠 Resposta:", response["response"])

        print("\n📚 Contexto:")
        for t in response["context"]["texts"]:
            print(t)
            print("\n" + "-" * 50 + "\n")
        for img in response["context"]["images"]:
            display_base64_image(img)

if __name__ == "__main__":
    main()

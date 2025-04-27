import os
import time
import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import re

# === 1. Função para extrair texto e imagens ===
def extract_pdf_contents(pdf_path):
    text = ""
    images = []
    tables = []

    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
            images.extend(page.get_images(full=True))

    with pdfplumber.open(pdf_path) as doc:
        for page in doc.pages:
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                df = pd.DataFrame(table)
                tables.append(df)

    return text, tables, images

# === 2. Função para limpar o texto ===
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = text.strip()
    return text

# === 3. Função para dividir o texto em chunks menores ===
def split_text(text, chunk_size=500):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]
    return chunks

# === 4. Função para gerar embeddings e salvar ===
def create_and_save_embeddings(chunks, save_folder, index_name="faiss_index.bin"):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(chunks)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    os.makedirs(save_folder, exist_ok=True)
    index_file_path = os.path.join(save_folder, index_name)
    faiss.write_index(index, index_file_path)

    print(f"💾 FAISS index salvo em: {index_file_path}")
    return index_file_path

# === 5. Função para processar um único PDF ===
def process_pdf(pdf_path):
    text, tables, images = extract_pdf_contents(pdf_path)
    cleaned_text = clean_text(text)
    chunks = split_text(cleaned_text)
    return {
        "text_chunks": chunks,
        "tables": tables,
        "images": images
    }

# === 6. Função para percorrer todas as subpastas e processar ===
def process_all_pdfs(root_folder, save_folder):
    all_chunks = []
    pdf_files = []

    # Captura todos os PDFs primeiro
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_files.append(os.path.join(subdir, file))

    total_files = len(pdf_files)
    print(f"📚 Total de arquivos PDF encontrados: {total_files}")

    if total_files == 0:
        print("⚠️ Nenhum arquivo PDF encontrado para processar.")
        return None

    start_time = time.time()

    for idx, pdf_path in enumerate(pdf_files, start=1):
        print(f"🔎 [{idx}/{total_files}] Processando: {os.path.basename(pdf_path)}")

        pdf_data = process_pdf(pdf_path)
        all_chunks.extend(pdf_data["text_chunks"])

    print(f"\n📄 Total de pedaços de texto extraídos: {len(all_chunks)}")

    index_path = create_and_save_embeddings(all_chunks, save_folder)

    elapsed_time = time.time() - start_time
    minutes, seconds = divmod(int(elapsed_time), 60)
    print(f"\n⏱️  Processamento completo em {minutes} min {seconds} seg.")

    return index_path

# === 7. Main App ===
if __name__ == "__main__":
    # Caminhos
    DOCUMENTS_FOLDER = os.path.join("data_extraction", "documentos_ufabc")
    PROCESSED_FOLDER = os.path.join("data_processed")

    print(f"🛠️ Iniciando processamento dos documentos na pasta: {DOCUMENTS_FOLDER}")
    index_path = process_all_pdfs(DOCUMENTS_FOLDER, PROCESSED_FOLDER)

    if index_path:
        print(f"\n✅ Embeddings criados e salvos em: {index_path}")
    else:
        print("\n⚠️ Processo finalizado sem criação de embeddings.")

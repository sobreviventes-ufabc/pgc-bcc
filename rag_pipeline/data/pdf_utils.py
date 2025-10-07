import time
import html
import re
import unicodedata
from unstructured.partition.pdf import partition_pdf

def extract_chunks_from_pdf(file_path):
    try:
        start_time = time.time()
        chunks = partition_pdf(
            filename=str(file_path),
            infer_table_structure=True,
            strategy="hi_res",
            languages=["por"],
            extract_image_block_types=["Image"],
            extract_image_block_to_payload=True,
            chunking_strategy="by_title",
            max_characters=3000,
            combine_text_under_n_chars=500,
            new_after_n_chars=1500,
        )
        print(f"{file_path.name}: {len(chunks)} chunks extraídos")
        return chunks
    except Exception as e:
        print(f"Erro ao processar {file_path.name}: {e}")
        return []

def limpar_html(html_text):
    if not html_text:
        return html_text
    html_text = html.unescape(html_text)
    html_text = unicodedata.normalize("NFKC", html_text)
    html_text = html_text.encode("utf-8", "ignore").decode("utf-8")
    html_text = re.sub(r"\s+", " ", html_text)
    html_text = re.sub(r"\s*\.\s*", " ", html_text)
    return re.sub(r"\s+", " ", html_text).strip()

def classify_chunks(chunks):
    texts, tables, images = [], [], []
    for chunk in chunks:
        if hasattr(chunk.metadata, "text_as_html") and chunk.metadata.text_as_html:
            tables.append(chunk.metadata.text_as_html)
        elif "CompositeElement" in str(type(chunk)):
            texts.append(chunk.text)
            for el in chunk.metadata.orig_elements:
                if "Image" in str(type(el)):
                    images.append(el.metadata.image_base64)
    return texts, tables, images
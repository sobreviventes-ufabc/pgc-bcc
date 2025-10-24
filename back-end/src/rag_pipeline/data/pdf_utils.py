import time
import html
import re
from unstructured.partition.pdf import partition_pdf
from data.tables import reestruturar_tabelas

def extract_chunks_from_pdf(file_path):
    """
    Extrai chunks de texto, tabelas e imagens de um PDF usando Unstructured.
    """
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
        print(f"{file_path.name}: {len(chunks)} chunks extraídos em {time.time()-start_time:.2f}s")
        return chunks
    except Exception as e:
        print(f"Erro ao processar {file_path.name}: {e}")
        return []


def limpar_html(html_text: str) -> str:
    """
    Limpeza leve de HTML/texto: normaliza entidades, acentuação e espaços.
    Pensado para rodar em tabelas (antes do BeautifulSoup).
    """
    if not html_text:
        return html_text
    html_text = html.unescape(html_text)
    #html_text = unicodedata.normalize("NFKC", html_text)
    html_text = html_text.encode("utf-8", "ignore").decode("utf-8")
    # Mantém estrutura, só corrige espaços extras
    html_text = re.sub(r"\s+", " ", html_text)
    return html_text.strip()

def classify_chunks(chunks):
    """
    Classifica os chunks em textos, tabelas (convertidas para Markdown) e imagens.

    - Tabelas (chunk.metadata.text_as_html):
        passam por limpar_html -> corrigir_tabela -> html_para_markdown.
    - Textos (CompositeElement):
        guardados como texto cru, sem limpar_html.
    - Imagens:
        extraídas em base64 dos orig_elements.
    """
    texts, tables, images = [], [], []

    for chunk in chunks:
        # Caso o Unstructured tenha identificado HTML (normalmente tabelas)
        if hasattr(chunk.metadata, "text_as_html") and chunk.metadata.text_as_html:
            html_bruto = chunk.metadata.text_as_html
            html_limpo = limpar_html(html_bruto)
            tables.append(html_limpo)

        # Caso seja texto corrido
        elif "CompositeElement" in str(type(chunk)):
            texts.append(chunk.text)  # aqui não roda limpar_html

            # Se o chunk original tiver imagens embutidas
            for el in getattr(chunk.metadata, "orig_elements", []):
                if "Image" in str(type(el)):
                    images.append(el.metadata.image_base64)
    
    tabelas_final = [reestruturar_tabelas(tbl) for tbl in tables]
    return texts, tabelas_final, images
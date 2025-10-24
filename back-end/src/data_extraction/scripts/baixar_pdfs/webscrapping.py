import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

JSON_ENTRADA = "lista_sites_docs_valid.json"
PASTA_BASE = os.path.join("..", "documentos_ufabc")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def criar_pasta(path):
    os.makedirs(path, exist_ok=True)

def limpar_nome(nome):
    return "".join(c if c.isalnum() or c in "._- " else "_" for c in nome)

def baixar_pdfs(url, pasta_destino):
    baixados = 0
    existentes = 0
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        links_pdf = soup.find_all("a", href=lambda href: href and href.lower().endswith(".pdf"))

        for link in links_pdf:
            href = link.get("href")
            pdf_url = urljoin(url, href)
            pdf_nome = limpar_nome(os.path.basename(urlparse(pdf_url).path))
            caminho_pdf = os.path.join(pasta_destino, pdf_nome)

            if not os.path.exists(caminho_pdf):
                print(f"🔽 Baixando: {pdf_nome} de {url}")
                with requests.get(pdf_url, headers=HEADERS, stream=True) as r:
                    r.raise_for_status()
                    with open(caminho_pdf, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                baixados += 1
            else:
                print(f"✅ Já existe: {pdf_nome}")
                existentes += 1
    except Exception as e:
        print(f"❌ Erro ao acessar {url}: {e}")
    return baixados, existentes

def percorrer_json(json_data, caminho_atual=[]):
    total_baixados = 0
    total_existentes = 0
    for chave, valor in json_data.items():
        nome_sanitizado = limpar_nome(chave)
        novo_caminho = caminho_atual + [nome_sanitizado]

        if isinstance(valor, dict):
            b, e = percorrer_json(valor, novo_caminho)
            total_baixados += b
            total_existentes += e
        elif isinstance(valor, str):
            pasta_destino = os.path.join(PASTA_BASE, *novo_caminho)
            criar_pasta(pasta_destino)
            b, e = baixar_pdfs(valor, pasta_destino)
            total_baixados += b
            total_existentes += e
    return total_baixados, total_existentes

def main():
    with open(JSON_ENTRADA, encoding="utf-8") as f:
        dados = json.load(f)

    baixados, existentes = percorrer_json(dados)
    total = baixados + existentes
    print("\n🏁 Processamento concluído.")
    print(f"📥 Arquivos baixados: {baixados}")
    print(f"📂 Arquivos já existentes: {existentes}")
    print(f"📊 Total de arquivos identificados: {total}")

if __name__ == "__main__":
    main()

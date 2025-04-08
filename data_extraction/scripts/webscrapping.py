import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Caminho para o JSON limpo
JSON_ENTRADA = "lista_sites_docs_valid.json"

# Pasta base para salvar os documentos
PASTA_BASE = os.path.join("..", "documentos_ufabc")

# Cabeçalhos para requisição
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Cria diretórios de forma segura
def criar_pasta(path):
    os.makedirs(path, exist_ok=True)

# Sanitiza nomes de arquivos/pastas
def limpar_nome(nome):
    return "".join(c if c.isalnum() or c in "._- " else "_" for c in nome)

# Faz o download de todos os PDFs de uma URL e salva na pasta correta
def baixar_pdfs(url, pasta_destino):
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
            else:
                print(f"✅ Já existe: {pdf_nome}")
    except Exception as e:
        print(f"❌ Erro ao acessar {url}: {e}")

# Percorre recursivamente o JSON
def percorrer_json(json_data, caminho_atual=[]):
    for chave, valor in json_data.items():
        nome_sanitizado = limpar_nome(chave)
        novo_caminho = caminho_atual + [nome_sanitizado]

        if isinstance(valor, dict):
            percorrer_json(valor, novo_caminho)
        elif isinstance(valor, str):
            pasta_destino = os.path.join(PASTA_BASE, *novo_caminho)
            criar_pasta(pasta_destino)
            baixar_pdfs(valor, pasta_destino)

# Execução principal
def main():
    with open(JSON_ENTRADA, encoding="utf-8") as f:
        dados = json.load(f)

    percorrer_json(dados)
    print("🏁 Todos os documentos foram processados.")

if __name__ == "__main__":
    main()

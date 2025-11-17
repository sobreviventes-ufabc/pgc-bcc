import json
import requests
from bs4 import BeautifulSoup
import csv
import os

# Função para verificar se a URL existe e se há PDFs
def verificar_url(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Não encontrada", 0
        soup = BeautifulSoup(response.text, 'html.parser')
        pdf_links = soup.find_all('a', href=lambda href: href and href.lower().endswith('.pdf'))
        return "OK", len(pdf_links)
    except Exception as e:
        return f"Erro ({str(e)[:50]})", 0

# Função recursiva para percorrer o JSON em formato de árvore
def percorrer_json(dados, caminho_atual=[], resultados=[]):
    for chave, valor in dados.items():
        novo_caminho = caminho_atual + [chave]
        if isinstance(valor, dict):
            percorrer_json(valor, novo_caminho, resultados)
        else:
            status, qtd_pdfs = verificar_url(valor)
            resultados.append({
                "Caminho": " > ".join(novo_caminho),
                "URL": valor,
                "Status da Página": status,
                "Possui PDFs": "Sim" if qtd_pdfs > 0 else "Não",
                "Quantidade de PDFs": qtd_pdfs
            })
    return resultados

# Caminho para o arquivo JSON
ARQUIVO_JSON = "lista_sites_docs.json"

# Nome do relatório
ARQUIVO_RELATORIO = "relatorio_prograd.csv"

# Execução
def main():
    with open(ARQUIVO_JSON, encoding="utf-8") as f:
        dados = json.load(f)

    print("🔍 Verificando URLs... Isso pode levar alguns minutos.")
    resultados = percorrer_json(dados)

    with open(ARQUIVO_RELATORIO, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
        writer.writeheader()
        writer.writerows(resultados)

    print(f"✅ Relatório gerado com sucesso: {ARQUIVO_RELATORIO}")

if __name__ == "__main__":
    main()

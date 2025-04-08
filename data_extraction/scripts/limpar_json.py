import json
import csv

# Arquivos
ARQUIVO_JSON_ENTRADA = "lista_sites_docs.json"
ARQUIVO_CSV_RELATORIO = "relatorio_prograd.csv"
ARQUIVO_JSON_LIMPO = "lista_sites_docs.json"

# Carrega as páginas válidas do CSV
def carregar_urls_validas(caminho_csv):
    urls_validas = set()
    with open(caminho_csv, encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            if linha["Status da Página"] == "OK" and linha["Possui PDFs"] == "Sim":
                urls_validas.add(linha["URL"])
    return urls_validas

# Função recursiva para limpar o JSON original
def limpar_json(data, urls_validas):
    if isinstance(data, dict):
        novo_dict = {}
        for chave, valor in data.items():
            if isinstance(valor, dict):
                sub_dict = limpar_json(valor, urls_validas)
                if sub_dict:  # Só adiciona se não estiver vazio
                    novo_dict[chave] = sub_dict
            elif isinstance(valor, str):
                if valor in urls_validas:
                    novo_dict[chave] = valor
        return novo_dict
    return data

# Execução principal
def main():
    with open(ARQUIVO_JSON_ENTRADA, encoding="utf-8") as f:
        dados_json = json.load(f)

    urls_validas = carregar_urls_validas(ARQUIVO_CSV_RELATORIO)

    dados_limpos = limpar_json(dados_json, urls_validas)

    with open(ARQUIVO_JSON_LIMPO, "w", encoding="utf-8") as f:
        json.dump(dados_limpos, f, indent=2, ensure_ascii=False)

    print(f"✅ JSON limpo salvo em: {ARQUIVO_JSON_LIMPO}")

if __name__ == "__main__":
    main()

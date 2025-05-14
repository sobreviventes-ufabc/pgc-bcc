from rag_pipeline.document_loader import load_documents_from_folder
from rag_pipeline.bmS_25 import create_bm25_index, query_bm25
from rag_pipeline.prompt_template import build_rag_prompt
from rag_pipeline.llmCall import send_prompt_to_llm

if __name__ == "__main__":
    docs = load_documents_from_folder("./data_processed")
    if not docs:
        print("Nenhum documento encontrado em ./data_processed. Verifique o caminho ou adicione arquivos .txt.")
        exit()
    retriever = create_bm25_index(docs)

    while True:
        question = input("\nDigite sua pergunta (ou 'sair'): ")
        if question.lower() == "sair":
            break

        docs_retrieved = query_bm25(retriever, question)
        prompt = build_rag_prompt(docs_retrieved, question)
        response = send_prompt_to_llm(prompt)
        print("\nResposta:\n", response)
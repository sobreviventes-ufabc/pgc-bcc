from matplotlib.colors import Normalize
from rag_pipeline.document_loader import load_documents_from_folder
from rag_pipeline.bmS_25 import create_bm25_index, query_bm25
from rag_pipeline.prompt_template import build_rag_prompt
from rag_pipeline.llmCall import send_prompt_to_llm
import re
import numpy as np

def normalize(text: str) -> str:
    return re.sub(r"[áàãâäéèêëíìîïóòõôöúùûüçÁÀÃÂÄÉÈÊËÍÌÎÏÓÒÕÔÖÚÙÛÜÇ]", " ", text)

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
    
        #normalizedQuestion = normalize(question)
        docs_retrieved = query_bm25(retriever, question)
        if not docs_retrieved:
            print("Nenhum documento relevante foi recuperado.")
            print("A resposta poderia estar incorreta ou baseada em conhecimento geral da LLM.\n")
            continue
        '''
        print("Documentos recuperados pelo BM25:\n")
        for i, (doc, score) in enumerate(docs_retrieved, 1):
            score_value = score
            if isinstance(score, np.ndarray):
                score_value = score.item() if score.size == 1 else float(score[0])
            print(f"Documento {i} (score: {score_value:.4f}):\n{doc[:300]}...\n{'-'*60}")
        '''
        #context_docs = [doc for doc, _ in docs_retrieved]
        prompt = build_rag_prompt(docs_retrieved, question)
        response = send_prompt_to_llm(prompt)
        print("\nResposta:\n", response)



'''
if __name__ == "__main__":
    while True:
        question = input("\nDigite sua pergunta (ou 'sair'): ")
        if question.lower() == "sair":
            break

        response = send_prompt_to_llm(question)  # envia direto a pergunta
        print("\nResposta:\n", response)
'''
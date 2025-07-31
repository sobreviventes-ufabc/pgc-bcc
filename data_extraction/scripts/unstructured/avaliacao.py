import os
import json
from pathlib import Path
from typing import List
from datasets import Dataset

# Importa as funções e a pipeline do seu arquivo app.py
from app import get_rag_pipeline, get_chat_model, build_prompt
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
from langchain.schema.document import Document

# Caminho do arquivo JSON de avaliação
EVAL_DATASET_PATH = "perguntas-apresentacao.json"

# --- Parte 1: Classe personalizada para Ragas usar seu LLM local ---
class LocalRagasLLM:
    """
    Classe para permitir que a biblioteca Ragas use seu LLM local.
    Ele usa a mesma lógica do seu app.py para obter o modelo.
    """
    def __init__(self):
        self.model = get_chat_model()
        self.output_parser = StrOutputParser()

    def generate_text(self, prompt: str) -> str:
        prompt_template = ChatPromptTemplate.from_messages([HumanMessage(content=prompt)])
        chain = prompt_template | self.model | self.output_parser
        return chain.invoke({})

    def generate_text_list(self, prompts: List[str]) -> List[str]:
        return [self.generate_text(p) for p in prompts]

# --- Parte 2: Execução da avaliação ---
if __name__ == "__main__":
    # 1. Carregar o dataset de avaliação
    print(f"Carregando dataset de avaliação de: {EVAL_DATASET_PATH}")
    if not os.path.exists(EVAL_DATASET_PATH):
        print(f"Erro: Arquivo '{EVAL_DATASET_PATH}' não encontrado.")
        exit()
        
    with open(EVAL_DATASET_PATH, 'r', encoding='utf-8') as f:
        eval_data = json.load(f)

    # 2. Inicializar o seu pipeline RAG, chamando a função de app.py
    chain = get_rag_pipeline()
    if not chain:
        print("Não foi possível inicializar a pipeline RAG. Saindo.")
        exit()
    
    # 3. Preparar o dataset para o Ragas
    questions = [item['pergunta'] for item in eval_data]
    ground_truths = [[item['resposta_esperada']] for item in eval_data]

    answers = []
    contexts = []
    for question in questions:
        try:
            print(f"Gerando resposta para a pergunta: {question[:50]}...")
            response = chain.invoke(question)
            answers.append(response['response'])
            
            # Adicionar o contexto. O formato de `ragas` é uma lista de strings.
            context_text = [t for t in response['context']['texts'] if t]
            if not context_text:
                context_text = [""]
            contexts.append(context_text)

        except Exception as e:
            print(f"Erro ao gerar resposta para '{question[:50]}...': {e}")
            answers.append("Erro ao gerar resposta.")
            contexts.append([""])
            
    dataset = Dataset.from_dict({
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths,
    })

    # 4. Inicializar o LLM para a avaliação do Ragas
    ragas_llm = LocalRagasLLM()

    # 5. Executar a avaliação
    print("\nIniciando a avaliação com Ragas...")
    results = evaluate(
        dataset,
        metrics=[
            faithfulness,
            answer_relevancy
        ],
        llm=ragas_llm
    )
    
    # 6. Exibir os resultados
    print("\n--- Resultados da Avaliação ---")
    print(results)
    print("\n--- Resultados em Tabela ---")
    print(results.to_pandas())
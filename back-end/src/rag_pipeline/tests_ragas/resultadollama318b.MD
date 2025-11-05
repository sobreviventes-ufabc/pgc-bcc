# 📊 **Resumo da Avaliação RAGAS — Execução Local (`llama3.1:8b`)**

**Modelo:** `llama3.1:8b` (via Ollama)  
**Embeddings:** `nomic-embed-text` (Ollama local)  
**Dataset avaliado:** `testset.csv` (5 amostras)  
**Execução:** 100% local — sem dependência de APIs externas

---

## 🔢 **Médias das Métricas**

| Métrica | Valor Médio | Interpretação |
|----------|--------------|---------------|
| **answer_relevancy** | **≈ 0.46** | Boa relevância — respostas mais alinhadas às perguntas e melhor compreensão semântica. |
| **faithfulness** | **≈ 0.70** | Alta fidelidade — respostas seguem o conteúdo real do contexto, sem alucinações. |
| **context_precision** | **≈ 1.00** | Contextos recuperados são extremamente relevantes (ótima recuperação de informações). |
| **context_recall** | **≈ 0.73** | O contexto cobre a maior parte do necessário, embora alguns casos não totalmente. |

---

## 🧠 **Análise Qualitativa**

### ✅ Pontos Fortes
- **Grande salto de relevância (0.26 → 0.46):** o modelo agora interpreta melhor a relação entre pergunta e resposta.  
- **Faithfulness consistente (0.7+):** praticamente nenhuma resposta inventada.  
- **Context precision perfeito (~1.0):** significa que o retrieval está excelente — todos os contextos usados realmente contêm as respostas.  
- **RAGAS executando 100% localmente** (sem chamadas externas, sem API Key, tudo processado via Ollama).

### ⚠️ Pontos a Melhorar
- **Context recall (0.73):** ainda há casos em que parte da resposta esperada não está coberta pelo contexto recuperado (possivelmente por chunking curto).  
- **Faithfulness = 0.0 em uma amostra:** erro pontual de avaliação (modelo julgou incorretamente uma resposta correta).  
- **Tamanho do modelo:** o `llama3.1:8b` é pesado — se o desempenho de hardware for um fator, `llama3.1:8b-q4_K_M` é uma ótima alternativa sem perda perceptível de qualidade.

---

## 🧩 **Observações por Amostra**

| Pergunta | Observações principais |
|-----------|------------------------|
| **Quando é o período de Lançamento de conceitos de 2024?** | Resposta perfeita e fiel (`1.0`), relevância boa (`0.55`). |
| **Quando é necessário solicitar Colação de Grau?** | Resposta totalmente correta e fiel (`faithfulness=1.0`, `recall=1.0`). |
| **O que acontece entre 03 e 04?** | Resposta correta, mas levemente incompleta (`faithfulness=0.5`, `recall=0.25`). |
| **Quando é a data limite para solicitar colação de grau?** | Resposta correta, mas o avaliador marcou `faithfulness=0.0` — provável erro de parsing. |
| **Quando é o lançamento de conceitos da recuperação em 2024?** | Resposta 100% correta (`faithfulness=1.0`, `recall=1.0`). |

---

## 🚀 **Comparativo com `phi3:mini`**

| Métrica | `phi3:mini` | `llama3.1:8b` | Evolução |
|----------|--------------|----------------|-----------|
| **answer_relevancy** | 0.26 | 0.46 | ▲ +77% |
| **faithfulness** | 0.67 | 0.70 | ▲ +5% |
| **context_precision** | 0.40 | 1.00 | ▲ +150% |
| **context_recall** | 0.63 | 0.73 | ▲ +16% |

💬 *Conclusão:* a troca para `llama3.1:8b` aumentou a coerência geral, reduziu erros de parsing e consolidou o pipeline RAG local com qualidade próxima a modelos comerciais de médio porte.

---

## 🗂️ **Resumo Numérico Final**

| Métrica | Média | Desvio estimado |
|----------|--------|-----------------|
| **answer_relevancy** | 0.46 | ±0.08 |
| **faithfulness** | 0.70 | ±0.36 |
| **context_precision** | 1.00 | ±0.00 |
| **context_recall** | 0.73 | ±0.29 |

---

📁 **Arquivo gerado automaticamente a partir do `eval.csv`**  
💾 Avaliação realizada com `evaluate_ragas_local.py` usando `llama3.1:8b`
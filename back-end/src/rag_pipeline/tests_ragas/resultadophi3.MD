# 📊 **Resumo da Avaliação RAGAS — Execução Local**

**Modelo:** `phi3:mini` (via Ollama)  
**Embeddings:** `nomic-embed-text` (Ollama local)  
**Dataset avaliado:** `testset.csv` (5 amostras)  
**Execução:** 100% local — sem dependência de APIs externas

---

## 🔢 **Médias das Métricas**

| Métrica | Valor Médio | Interpretação |
|----------|--------------|---------------|
| **answer_relevancy** | **≈ 0.26** | Relevância de resposta baixa (modelo entende parcialmente as perguntas). |
| **faithfulness** | **≈ 0.67** | Boa fidelidade ao contexto — respostas geralmente corretas e não inventadas. |
| **context_precision** | **≈ 0.40** | Contextos recuperados úteis em parte, mas nem sempre diretamente relacionados à resposta. |
| **context_recall** | **≈ 0.63** | O modelo geralmente encontra o contexto certo, mas às vezes incompleto. |

---

## 🧠 **Análise Qualitativa**

### ✅ Pontos Fortes
- **Fidelidade alta (0.67–1.0):** o modelo baseia suas respostas no contexto recuperado e não alucina.  
- **Context recall razoável:** o retriever encontra pelo menos parte do trecho relevante em quase todos os casos.  
- **Pipeline totalmente funcional localmente:** sem dependência de OpenAI, API key ou rede externa.

### ⚠️ Pontos a Melhorar
- **Answer relevancy baixo (0.26):** `phi3:mini` é pequeno (3.8B) e o RAGAS exige que o modelo avalie a coerência da própria resposta — ele tende a errar nessa autoavaliação.  
- **Context precision (0.4):** alguns contextos recuperados trazem muito ruído — pode ser melhorado ajustando o chunking ou os embeddings (ex: tamanho de bloco, overlap, ou troca para `mxbai-embed-large` se quiser algo local mais robusto).

---

## 🧩 **Observações por Amostra**

| Pergunta | Observações principais |
|-----------|------------------------|
| **Quando é o período de Lançamento de conceitos de 2024?** | Resposta correta, mas `answer_relevancy = 0.0` — erro de parsing do modelo avaliador. |
| **Quando é necessário solicitar Colação de Grau?** | Resposta parcialmente fiel (`faithfulness=0.5`), contexto bom (`precision≈1.0`). |
| **O que acontece entre 03 e 04?** | Resposta correta mas incompleta (`relevancy=0.36`, `faithfulness=0.33`). |
| **Quando é a data limite para solicitar colação de grau?** | Contextos bons mas parciais (`precision=0`, `recall=0.4`). |
| **Quando é o lançamento de conceitos da recuperação em 2024?** | Excelente fidelidade (`1.0`), relevância moderada (`0.48`). |

---

## 🚀 **Conclusão Geral**

- ✅ **Funcionamento técnico:** pipeline local validado, comunicação com Ollama e embeddings confirmada.  
- 💡 **Desempenho:** coerente com um modelo pequeno (`phi3:mini`) — respostas corretas, mas avaliação automática punitiva.  
- 📈 **Próximos passos sugeridos:**
  1. Testar com `llama3:8b` ou `mistral:7b` no lugar de `phi3:mini` → tende a aumentar `answer_relevancy` e `faithfulness`.
  2. Ajustar chunking de documentos (por exemplo, blocos de 500 tokens com 100 de overlap).
  3. Usar `reranker` leve local (ex: `bge-reranker-v2`) para subir `context_precision`.

---

## 🗂️ **Resumo Numérico Final**

| Métrica | Média | Desvio estimado |
|----------|--------|-----------------|
| **answer_relevancy** | 0.26 | ±0.20 |
| **faithfulness** | 0.67 | ±0.29 |
| **context_precision** | 0.40 | ±0.40 |
| **context_recall** | 0.63 | ±0.26 |

---

📁 **Arquivo gerado automaticamente a partir do `eval.csv`**  
💾 Avaliação realizada com `evaluate_ragas_local.py`
# 📊 **Resumo da Avaliação RAGAS**

**Modelo:** `gpt-4o-mini`  
**Embeddings:** `nomic-embed-text` (Ollama local)  
**Dataset avaliado:** `testset.csv` (50 amostras)  
**Configuração:** `CHUNK_SIZE=800`, `CHUNK_OVERLAP=100`, `DELAY=1.5s`

---

## 🔢 **Médias das Métricas**

| Métrica | Valor Médio | Interpretação |
|----------|--------------|---------------|
| **answer_relevancy** | **≈ 0.94** | Excelente relevância — respostas fortemente alinhadas às perguntas. |
| **faithfulness** | **≈ 0.85** | Alta fidelidade ao contexto — poucas ou nenhuma alucinação. |
| **context_precision** | **≈ 0.99** | Contextos recuperados extremamente precisos e relevantes. |
| **context_recall** | **≈ 0.90** | O modelo recupera praticamente todos os trechos necessários. |

---

## 🧠 **Análise Qualitativa**

### ✅ Pontos Fortes
- **Altíssima precisão de contexto (0.99):** o retriever está retornando apenas trechos relevantes — excelente segmentação e embeddings bem calibrados.  
- **Relevância de resposta quase perfeita (0.94):** o modelo compreende as perguntas e responde com alta coerência sem desviar do tema.  
- **Execução totalmente local:** pipeline validado, independente de APIs externas e com desempenho estável.  
- **Boas médias gerais:** todos os scores acima de 0.8, mostrando ótimo equilíbrio entre geração e avaliação.

### ⚠️ Pontos a Melhorar
- **Faithfulness (0.85):** apesar de alto, ainda há pequenos casos onde a resposta não é 100% ancorada no contexto. Pode ser refinado ajustando o prompt de geração ou aumentando `num_ctx` do modelo avaliador.  
- **Context recall (0.9):** ocasionalmente, parte do contexto relevante pode estar fora do chunk recuperado — experimentar `CHUNK_OVERLAP=150` pode ajudar a chegar a 1.0.  

---

## 🧩 **Observações Gerais**

- O modelo `gpt-4o-mini` demonstra **grande consistência** na interpretação das perguntas.

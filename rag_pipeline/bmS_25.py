import bm25s

def create_bm25_index(docs):
    """
    Indexador BM25 a partir de uma lista de documentos (strings).
    """
    print(f"Antes de corrigir: tipo do primeiro doc: {type(docs[0])}")
    print(f"Conteúdo bruto: {repr(docs[0])[:200]}")

    # Agora corrige se não for string
    docs = [doc if isinstance(doc, str) else " ".join(doc) for doc in docs]

    print(f"Depois de corrigir: {repr(docs[0])[:200]}")
    print(f"Total de documentos indexados: {len(docs)}")

    corpus_tokens = bm25s.tokenize(docs)
    retriever = bm25s.BM25(corpus=docs)
    retriever.index(corpus_tokens)
    return retriever

def query_bm25(retriever, query, top_k=10):
    """
    Busca BM25 usando o retriever e retorna os melhores documentos.
    """
    query_tokens = bm25s.tokenize(query)
    print(f"Tokens da query normalizada: {query_tokens}")
    docs, scores = retriever.retrieve(query_tokens, k=top_k)
    docs = [str(doc) for doc in docs]
    #for i, doc in enumerate(docs[:5]):
    #    print(f"\nDoc {i+1}:\n{repr(doc[:300])}")
    #doc_score_pairs = list(zip(docs, scores))
    #doc_score_pairs.sort(key=lambda x: x[1], reverse=True)

    return docs
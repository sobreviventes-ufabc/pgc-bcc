import bm25s

def build_corpus(file_paths):
    """
    Carrega documentos de uma lista de arquivos e retorna como lista de strings.
    """
    docs = []
    for file in file_paths:
        with open(file, "r", encoding="utf-8") as f:
            docs.append(f.read())
    return docs

def create_bm25_index(docs):
    """
    Indexador BM25 a partir de uma lista de documentos (strings).
    """
    corpus_tokens = bm25s.tokenize(docs)
    retriever = bm25s.BM25(corpus=docs)
    retriever.index(corpus_tokens)
    return retriever

def query_bm25(retriever, query, top_k=5):
    """
    Busca BM25 usando o retriever e retorna os melhores documentos.
    """
    query_tokens = bm25s.tokenize(query)
    docs, scores = retriever.retrieve(query_tokens, k=top_k)
    docs = [str(doc) for doc in docs]
    return docs
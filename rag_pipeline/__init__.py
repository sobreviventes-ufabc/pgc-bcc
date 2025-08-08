"""
Top-level package for the multi-modal RAG project.

This package contains utilities for extracting, summarizing and retrieving
information from PDF documents using a multi-vector retriever. The code has
been refactored from a single monolithic script into a modular structure to
improve maintainability and reuse.

To get started, import and call the ``get_rag_pipeline`` function from
:mod:`rag_pipeline.core.retriever_pipeline` or run ``python -m rag_pipeline.main``.
"""

__all__ = [
    "core",
    "data",
    "utils",
    "config",
    "api",
    "main"
]
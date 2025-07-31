"""Top-level package for the multi‑modal RAG project.

This package contains utilities for extracting, summarising and retrieving
information from PDF documents using a multi‑vector retriever. The code has
been refactored from a single monolithic script into a modular structure to
improve maintainability and reuse. To get started, import and call the
``run_pipeline`` function from :mod:`rag_project.pipeline` or invoke
``python -m rag_project.cli`` from the command line.
"""

__all__ = [
    "config",
    "models",
    "utils",
    "pdf_processing",
    "summarisation",
    "retrieval",
    "pipeline",
]
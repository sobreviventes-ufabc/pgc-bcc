#!/usr/bin/env bash
ollama serve &
# You can add other commands here if needed, e.g., to list models
ollama pull nomic-embed-text:latest
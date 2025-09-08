FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    poppler-utils \
    libmagic1 \
    curl \
    && apt-get clean

# Install Ollama CLI
RUN curl -fsSL https://ollama.com/download/linux -o ollama-install.sh && \
    bash ollama-install.sh && \
    rm ollama-install.sh

# Set environment variables for Ollama
ENV OLLAMA_HOST=0.0.0.0:8080
ENV OLLAMA_MODELS=/models
ENV OLLAMA_DEBUG=false
ENV OLLAMA_KEEP_ALIVE=-1
ENV MODEL=gemma2:9b

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip wheel && \
    pip install -r requirements.txt && \
    pip install unstructured.pytesseract unstructured-inference pi-heif

# Copy application code
COPY . .

# Expose port 80
EXPOSE 80

# Start the FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80"]
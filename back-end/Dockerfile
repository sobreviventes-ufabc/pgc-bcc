FROM public.ecr.aws/lambda/python:3.13

# Install system dependencies required by OpenCV and unstructured
RUN dnf install -y \
    mesa-libGL \
    glib2 \
    libSM \
    libXext \
    libXrender \
    && dnf clean all

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Required to make SQLlite3 work for Chroma.
RUN pip install pysqlite3-binary

# Install the specified packages
RUN pip install -r requirements.txt --upgrade

# Install Ollama (adjust version and architecture as needed)
# Downloading the correct binary for x86_64/amd64 architecture
RUN curl -L https://ollama.com/download/ollama-linux-amd64 -o /usr/local/bin/ollama \
    && chmod +x /usr/local/bin/ollama

# Create a directory for Ollama models and data
RUN mkdir -p /root/.ollama

# Start Ollama server in background and pull the model
# Using a single RUN command with proper wait to ensure the process completes
COPY src/run-ollama.sh /tmp/run-ollama.sh
RUN chmod +x /tmp/run-ollama.sh && \
    ollama serve & \
    OLLAMA_PID=$! && \
    sleep 5 && \
    ollama pull nomic-embed-text:latest && \
    kill $OLLAMA_PID || true

# For local testing.
EXPOSE 8000

# Set IS_USING_IMAGE_RUNTIME Environment Variable
ENV IS_USING_IMAGE_RUNTIME=True

# Copy necessary source files
COPY src/rag_pipeline ${LAMBDA_TASK_ROOT}/rag_pipeline
COPY src/.cache_chunks ${LAMBDA_TASK_ROOT}/.cache_chunks
# COPY src/data_extraction ${LAMBDA_TASK_ROOT}/data_extraction


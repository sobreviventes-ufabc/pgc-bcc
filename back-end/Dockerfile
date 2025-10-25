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

# Install CPU-only torch first to prevent GPU version installation
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the packages
RUN pip install --no-cache-dir -r requirements.txt --upgrade && \
    # Clean up pip cache and unnecessary files
    pip cache purge

# For local testing.
EXPOSE 8000
# Set IS_USING_IMAGE_RUNTIME Environment Variable
ENV IS_USING_IMAGE_RUNTIME=True

# Copy necessary source files
COPY src/rag_pipeline ${LAMBDA_TASK_ROOT}/rag_pipeline
COPY src/.cache_chunks ${LAMBDA_TASK_ROOT}/.cache_chunks
# COPY src/data_extraction ${LAMBDA_TASK_ROOT}/data_extraction


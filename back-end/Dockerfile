FROM public.ecr.aws/lambda/python:3.13

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Required to make SQLlite3 work for Chroma.
RUN pip install pysqlite3-binary

# Install the specified packages
RUN pip install -r requirements.txt --upgrade

# For local testing.
EXPOSE 8000
# Set IS_USING_IMAGE_RUNTIME Environment Variable
ENV IS_USING_IMAGE_RUNTIME=True

# Install system dependencies required by OpenCV and unstructured
RUN dnf install -y \
    mesa-libGL \
    glib2 \
    libSM \
    libXext \
    libXrender \
    && dnf clean all

# Copy necessary source files
COPY src/rag_pipeline ${LAMBDA_TASK_ROOT}/rag_pipeline
COPY src/.cache_chunks ${LAMBDA_TASK_ROOT}/.cache_chunks
# COPY src/data_extraction ${LAMBDA_TASK_ROOT}/data_extraction


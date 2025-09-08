# 🤖 RAG Project Documentation

This project implements a Retrieval-Augmented Generation (RAG) system using FastAPI and various machine learning models. It is designed to extract, process, and query information from PDF documents and other data sources.

## 🛠️ Project Structure

```
rag-project
├── Dockerfile                # Defines the Docker image for the application
├── requirements.txt          # Lists all Python dependencies
├── data_extraction           # Contains files for extracting data from documents
├── data_processed            # Stores processed data, including extracted text and embeddings
├── rag_pipeline              # Main application code
│   ├── api.py                # FastAPI application with endpoints for querying the model
│   ├── main.py               # Entry point for running the application in CLI
│   ├── core                  # Core functionalities and models
│   ├── data                  # Utilities for data processing
│   ├── utils                 # Utility functions for displaying images and helpers
├── .cache_chunks             # Caches processed data, such as chunks and summaries
└── README.md                 # Documentation for setup and usage
```

## 🚀 Getting Started

### Prerequisites

- Docker installed on your machine
- Access to an AWS EC2 instance (if deploying there)

### Setup Instructions

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd rag-project
   ```

2. **Build the Docker image**:

   ```bash
   docker build -t rag-project .
   ```

3. **Run the Docker container**:

   ```bash
   docker run -p 80:80 \
     -v $(pwd)/data_extraction:/app/data_extraction \
     -v $(pwd)/data_processed:/app/data_processed \
     -v $(pwd)/.cache_chunks:/app/.cache_chunks \
     rag-project
   ```

   This command maps the local directories to the container, allowing the application to access the necessary files.

### Accessing the API

You can access the API at `http://<EC2_INSTANCE_IP>:80/ask` and send requests as needed.

### Example Request

```bash
curl --request POST \
  --url http://<EC2_INSTANCE_IP>:80/ask \
  --header 'Content-Type: application/json' \
  --data '{
    "question": "o que é PET"
}'
```

## 📦 Dependencies

The project relies on the following Python packages:

- langchain==0.3.26
- langchain-community==0.3.26
- chromadb>=0.5.4
- langchain-ollama>=0.2.0
- langchain-openai>=0.2.0
- langchain-groq>=0.1.0
- ollama>=0.1.9
- httpx>=0.24.0
- fastapi>=0.110
- uvicorn[standard]>=0.29
- pydantic>=2.6
- anyio>=4.0
- unstructured>=0.14.0
- pdfminer.six>=20221105
- pdf2image>=1.17.0
- pikepdf>=8.0.0
- Pillow>=9.5.0
- opencv-python>=4.8.0.76
- pytesseract>=0.3.10
- lxml>=4.9.0
- numpy>=1.24.0
- ipython>=8.12.0

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
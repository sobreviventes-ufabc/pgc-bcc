"""Custom embeddings implementation for Nomic API."""
import requests
import logging
from typing import List
from langchain_core.embeddings import Embeddings

# Configure logger
logger = logging.getLogger(__name__)


class NomicEmbeddings(Embeddings):
    """Custom embeddings class using Nomic API."""
    
    def __init__(self, api_key: str, model: str = "nomic-embed-text-v1.5"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api-atlas.nomic.ai/v1/embedding/text"
        logger.info(f"NomicEmbeddings initialized with model: {model}")
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents using Nomic API."""
        logger.info(f"embed_documents called with {len(texts)} texts")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "texts": texts,
                "task_type": "search_document"
            }
            
            logger.debug(f"Sending request to Nomic API: {self.api_url}")
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            embeddings = result.get("embeddings", [])
            logger.info(f"Successfully embedded {len(embeddings)} documents")
            return embeddings
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Nomic API for embed_documents: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}, Response body: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in embed_documents: {e}", exc_info=True)
            raise
    
    def embed_query(self, text: str) -> List[float]:
        """Embed a query using Nomic API."""
        logger.info(f"embed_query called with text length: {len(text)}")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "texts": [text],
                "task_type": "search_query"
            }
            
            logger.debug(f"Sending request to Nomic API: {self.api_url}")
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            embeddings = result.get("embeddings", [[]])
            embedding = embeddings[0] if embeddings else []
            logger.info(f"Successfully embedded query, embedding dimension: {len(embedding)}")
            return embedding
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Nomic API for embed_query: {e}")
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f"Response status: {e.response.status_code}, Response body: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in embed_query: {e}", exc_info=True)
            raise

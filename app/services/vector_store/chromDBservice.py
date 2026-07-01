from app.utils.logger import get_logger
import chromadb
from typing import Dict, Any

logger = get_logger(__name__)

class ChromaDBService:
    def __init__(self, client: chromadb.Client, collection_name: str = "embedding_collection"):
        self.client = client
        self.collection = client.get_or_create_collection(name = collection_name)

    def add_document(self, document_id : str, chunks : list[dict]) -> None:
        """Add a document to the ChromaDB."""
        try:
            self.collection.add(
                embeddings=[chunk["embedding"] for chunk in chunks],
                documents=[chunk["text"] for chunk in chunks],
                metadatas=[{
                    "chunk_id" : chunk["chunk_id"],
                    "start_index" : chunk["start_index"],
                    "end_index" : chunk["end_index"],
                    "document_id" : document_id
                } for chunk in chunks],
                ids=[chunk["chunk_id"] for chunk in chunks]
            )
            logger.info(f"Document added with ID: {document_id}")
            return None
        except Exception as e:
            logger.exception(f"Error adding document to ChromaDB: {e}")
            raise

    
    def search(self, query_embeddings: list[float], top_k: int = 5) -> Dict[str, Any]:
        """Search for similar documents based on query embeddings."""
        try:
            results = self.collection.query(
                query_embeddings=query_embeddings,
                n_results=top_k
            )
            return results
        except Exception as e:
            logger.exception(f"Error searching in ChromaDB: {e}")
            raise
    



from app.utils.logger import get_logger
from typing import List, Dict
from app.services.vector_store.chromDBservice import ChromaDBService


logger = get_logger(__name__)

class RetrieverDBService:
    def __init__(self, chromadb_service : ChromaDBService):
        self.chromadb_service = chromadb_service
    
    def retrieve_chunks(self, query_embedding : list[float], top_k : int = 3) -> list[dict]:
        """Retrieve relevant chunks based on query embedding."""
        try:
            retrieved_chunks = self.chromadb_service.search(
                query_embeddings=query_embedding,
                top_k = top_k
            )
            retrieved_chunks = [
                {
                    "text": retrieved_chunks["documents"][0][i],
                    #"embedding" : retrieved_chunks["embeddings"][0][i],
                    "metadata" : retrieved_chunks["metadatas"][0][i],
                    "id" : retrieved_chunks["ids"][0][i],
                    "distance" : retrieved_chunks["distances"][0][i],
                    "rank" : i + 1
                } for i in range(len(retrieved_chunks["ids"][0]))
            ]
            logger.info(f"Retrieved {len(retrieved_chunks)} chunks for query embedding")
            return retrieved_chunks
        except Exception as e:
            logger.exception(f"Error retrieving from ChromaDB: {e}")
            raise








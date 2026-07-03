from app.utils.logger import get_logger
from typing import List, Dict
from app.services.vector_store.chromDBservice import ChromaDBService
from app.config.settings import settings


logger = get_logger(__name__)

class RetrieverDBService:
    def __init__(self, chromadb_service : ChromaDBService, threshold : float = settings.rag_threshold):
        self.chromadb_service = chromadb_service
        self.threshold = threshold
    
    def retrieve_chunks(self, query_embedding : list[float], top_k : int = 3) -> list[dict]:
        """Retrieve relevant chunks based on query embedding."""
        try:
            search_results = self.chromadb_service.search(
                query_embeddings=query_embedding,
                top_k = top_k
            )
            filtered_items = [
            (doc, meta, id_, dist)
            for doc, meta, id_, dist in zip(
                search_results["documents"][0],
                search_results["metadatas"][0],
                search_results["ids"][0],
                search_results["distances"][0],
    )
            if dist <= self.threshold
]

            filtered_chunks = [
             {
            "text": doc,
            "metadata": meta,
            "id": id_,
            "distance": dist,
            "rank": rank,
            }
          for rank, (doc, meta, id_, dist) in enumerate(filtered_items, start=1)
]
            logger.info(f"Retrieved {len(filtered_chunks)} chunks for query embedding")
            return filtered_chunks
        except Exception as e:
            logger.exception(f"Error retrieving from ChromaDB: {e}")
            raise













from app.utils.logger import get_logger
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from app.exceptions.pdf_exception import RetrieveProcessingError
from typing import List, Dict, Any

logger = get_logger(__name__)

class RetrieverService:
    def retrieve(self, query_embedding : List[float], embeddings_chunks : List[Dict[str, Any]], top_k : int = 3) -> List[Dict[str, Any]]:
        try:
            logger.info(f"Retrieving top {top_k} chunks for query")
            document_embeddings = [chunk["embedding"] for chunk in embeddings_chunks]
            scores = cosine_similarity([query_embedding], document_embeddings)[0]
            top_k_indices = np.argsort(scores)[::-1][:top_k]
            result = []
            for i, index in enumerate(top_k_indices):
                result.append({
                    **embeddings_chunks[index],
                    "score": float(scores[index]),
                    "rank": i + 1
                })
            logger.info(f"Successfully retrieved {len(result)} chunks for query")
            return result
        except Exception as e:
            logger.exception("Error retrieving chunks")
            raise RetrieveProcessingError("Failed to retrieve chunks") from e





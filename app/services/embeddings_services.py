from app.utils.logger import get_logger
from sentence_transformers import SentenceTransformer

from app.exceptions.pdf_exception import EmbeddingProcessingError

logger = get_logger(__name__)

class EmbeddingsService:
    """
    Service responsible for creating embeddings for chunks.
    """
    def __init__(self, model_name : str = "sentence-transformers/all-MiniLM-L6-v2"):
        try:
            self._model_name = model_name
            self._model = SentenceTransformer(model_name)
            logger.info(f"Embeddings service initialized with model: {model_name}")
        except Exception as e:
            logger.exception("Error initializing EmbeddingsService")
            raise EmbeddingProcessingError("Failed to initialize EmbeddingsService") from e
    
    def embed_chunks(self, chunks : list[dict]) -> list[dict]:
        logger.info(f"Creating embeddings for {len(chunks)} chunks")
        try:
            texts = [chunk["text"] for chunk in chunks]
            embeddings = self._model.encode(texts, convert_to_numpy=True)
            embedded_chunks = []
            for chunk, embedding in zip(chunks, embeddings):
                embedded_chunks.append({
                    **chunk,
                    "embedding" : embedding.tolist()
                })
            logger.info(f"Successfully created embeddings for {len(chunks)} chunks")
            return embedded_chunks
        except Exception as e:
            logger.exception("Error creating embeddings for chunks")
            raise EmbeddingProcessingError("Failed to create embeddings for chunks") from e


embeddings_service_instance = EmbeddingsService()




from app.utils.logger import get_logger
from uuid import uuid4
from app.exceptions.pdf_exception import ChunkProcessingError
from langchain_text_splitters import RecursiveCharacterTextSplitter

logger= get_logger(__name__)

class ChunkService:
    @staticmethod
    def create_chunks(text : str, chunk_size : int = 500, overlap : int = 100) -> list[dict]:

        if overlap >= chunk_size:
            raise ChunkProcessingError("Overlap must be strictly less than chunk_size to prevent infinite loops.")

        if not text:
            raise ChunkProcessingError("Text cannot be empty for chunking.")

        logger.info(f"Starting Chunking Process with chunk_size: {chunk_size} and overlap: {overlap}")
        start = 0
        chunks = []

        try:
            while start < len(text):
                end = start + chunk_size
                chunk = text[start:end]
                chunks.append({
                    "chunk_id" : str(uuid4()),
                    "text" : chunk,
                    "start_index" : start,
                    "end_index" : end,
                })
                start += chunk_size - overlap
        except Exception as e:
            logger.exception("Error chunking text")
            raise ChunkProcessingError("Failed to chunk text") from e
        
        logger.info(f"Finished Chunking Process. Total chunks: {len(chunks)}")

        return chunks











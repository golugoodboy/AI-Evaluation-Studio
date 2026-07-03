from app.utils.logger import get_logger
from app.exceptions.pdf_exception import RecursiveChunkProcessingError
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config.settings import settings
from typing import List, Dict
from uuid import uuid4


logger= get_logger(__name__)

class ChunkService:
    def __init__(self) -> None:
        self.chunk_size = int(settings.chunk_size)
        self.chunk_overlap = int(settings.overlap)
        self.splitter = RecursiveCharacterTextSplitter(
            separators = ["\n\n", "\n",". ","? ","! "," ",""],
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def create_chunks(self, text : str) -> List[Dict]:
        if not text:
            raise RecursiveChunkProcessingError("Text cannot be empty for chunking.")

        logger.info(f"Starting Chunking Process with chunk_size: {self.chunk_size} and chunk_overlap: {self.chunk_overlap}")

        try:
            split_text = self.splitter.split_text(text)
            chunks = []
            for chunk in split_text:
                chunks.append({
                    "chunk_id" : str(uuid4()),
                    "text" : chunk
                })
            return chunks
        except Exception as e:
            logger.exception("Error chunking text")
            raise RecursiveChunkProcessingError("Failed to chunk text") from e







     











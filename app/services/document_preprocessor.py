from pathlib import Path
from typing import Dict, Any

from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.utils.logger import get_logger

logger = get_logger(__name__)

class DocumentProcessor:
    def __init__(self,pdf_service : PDFService,chunk_service : ChunkService):
        self._pdf_service = pdf_service
        self._chunk_service = chunk_service

    def process_document(self, pdf_path : Path  ) -> Dict[str, Any]:
        logger.info(f"Processing PDF located at {pdf_path}")

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found at {pdf_path}")

        extracted_data = self._pdf_service.extract_text(pdf_path)
        text = extracted_data["text"]
        chunks = self._chunk_service.create_chunks(text)

        return {
            "document" : {
                "title" : pdf_path.name,
                "page_count" : extracted_data["page_count"],
                "content" : text
            },
            "chunks": chunks
        }





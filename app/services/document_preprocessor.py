from uuid import uuid4
from typing import Dict, Any
from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.services.embeddings_services import EmbeddingsService
from app.utils.logger import get_logger
from app.services.document_storage_service import DocumentStorageService
from pathlib import Path
from app.services.vector_store.chromDBservice import ChromaDBService

logger = get_logger(__name__)

class DocumentProcessor:
    def __init__(self, pdf_service: PDFService, chunk_service: ChunkService, embedding_service: EmbeddingsService, storage_service: DocumentStorageService, chromadb_service : ChromaDBService):
        self._pdf_service = pdf_service
        self._chunk_service = chunk_service
        self._embedding_service = embedding_service
        self._storage_service = storage_service
        self._chromadb_service = chromadb_service

    def process_document(self, pdf_path: Path, document_id: str = None) -> Dict[str, Any]:
        logger.info(f"Processing PDF located at {pdf_path}")

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found at {pdf_path}")

        if document_id is None:
            document_id = str(uuid4())

        extracted_data = self._pdf_service.extract_text(pdf_path)
        text = "\n\n".join([page["text"] for page in extracted_data["pages"]])
        chunks = self._chunk_service.create_chunks(text)
        embeddings_chunks = self._embedding_service.embed_chunks(chunks)
        self._storage_service.save_document(
            document_id=document_id,
            data={
                    "document_id" : document_id,
                    "title": pdf_path.name,
                    "page_count": extracted_data["page_count"],
                    "content": text,
                    "chunks": chunks
                }
        )
        self._chromadb_service.add_document(document_id, embeddings_chunks)
        logger.info("PDF processed successfully")
        return {
            "document_id": document_id,
            "chunk_count": len(embeddings_chunks)
        }







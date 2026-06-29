from typing import List, Dict, Any
from app.utils.logger import get_logger
import json
from pathlib import Path
from app.exceptions.pdf_exception import DocumentStorageError
from app.config.settings import settings



logger = get_logger(__name__)

class DocumentStorageService:
    def __init__(self):
        self.base_dir = Path(settings.base_dir) / "data" / "processed"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
    def save_document(self, document_id: str, data: dict) -> None:
        try:
            file_path = Path(self.base_dir) / f"{document_id}.json"
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Document saved successfully: {document_id}")
        except Exception as e:
            logger.error(f"Failed to save document {document_id}: {str(e)}", exc_info=True)
            raise DocumentStorageError(f"Failed to save document {document_id}") from e
    
    def load_document(self, document_id: str) -> Dict[str, Any] | None:
        try:
            file_path = Path(self.base_dir) / f"{document_id}.json"
            if not file_path.exists():
                logger.error(f"Document not found: {document_id}")
                raise DocumentStorageError(f"Document not found: {document_id}")
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            logger.error(f"Failed to get document {document_id}: {str(e)}", exc_info=True)
            raise DocumentStorageError(f"Failed to get document {document_id}") from e




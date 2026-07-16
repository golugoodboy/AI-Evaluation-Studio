from app.utils.logger import get_logger
from typing import Dict, Any
from pathlib import Path
from datetime import datetime
import pymupdf

logger = get_logger(__name__)

class MetadataExtractorService:
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        logger.info(f"Extracting metadata from file :{file_path.name}")
        try:
            with pymupdf.open(file_path) as doc:
                pdf_metadata = doc.metadata
            
        except Exception as e:
            logger.exception(f"Error extracting metadata from {file_path.name}")
            raise PDFMetadataError(f"Failed to extract metadata from {file_path.name}") from e
        return {
            **pdf_metadata,
            "title": "...",
            "author": "...",
            "subject": "...",
            "keywords": [...],
            "language": None,
            "publisher": None,
            "creation_date": "...",
            "modification_date": "...",
        }






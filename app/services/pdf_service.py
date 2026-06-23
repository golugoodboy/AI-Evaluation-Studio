import fitz
from pathlib import Path
from app.utils.logger import get_logger
from app.exceptions.pdf_exception import PDFProcessingError

logger = get_logger(__name__)

class PDFService:
    """
    Service Responsible for reading PDF documents and extracting text.
    """
    @staticmethod
    def extract_text(file_path: Path) -> dict:
        logger.info(f"Extracting text from PDF : {file_path.name}")
        try:
            document_text = []
            with fitz.open(file_path) as document:
                for page in document:
                    document_text.append(page.get_text())
            logger.info(f"Extracted the file {file_path.name} Successfully and extracted {len(document_text)} pages.")
            final_text = "\n\n".join(document_text).strip()
            if not final_text:
                logger.warning(f"No text could be extracted from the {file_path.name}.It might be scanned images or protected.")
            return {
                "text": final_text,
                "page_count": len(document_text),
                "word_count": len(final_text.split()),
                "character_count": len(final_text),
            }
        except Exception as e:
            logger.exception(f"Error extracting text from : {file_path.name}")
            raise PDFProcessingError(f"Failed to process PDF : {file_path.name}") from e








                






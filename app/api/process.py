from fastapi import APIRouter
from app.utils.logger import get_logger
from app.config.settings import settings
from app.models.api_response import APIResponse
from app.services.pdf_service import PDFService
from app.exceptions.pdf_exception import PDFProcessingError


logger = get_logger(__name__)
router = APIRouter(prefix = "/process",tags = ["Process"])

@router.post("/{document_id}")
def process_document(document_id: str):
    logger.info(f"Received request to process document: {document_id}")
    filepath = settings.base_dir / "data" / "documents" / f"{document_id}.pdf"

    if not filepath.exists():
        logger.warning(f"File not found : {document_id}")
        return APIResponse(success=False, message="Document not found", data=None)

    try:
        extracted_data = PDFService.extract_text(filepath)
        text = extracted_data["text"]
        if not text:
            logger.warning(f"No text extracted from {document_id}.")
            return APIResponse(success=False, message="Document is empty or corrupted or may contain images or tables.", data=None)
        
        logger.info(f"Successfully extracted text from {document_id}")
        return APIResponse(success=True, message="Document processed successfully", data={"document_id": document_id, "text_preview": text[:100] + "..." if len(text) > 100 else text, "page_count": extracted_data["page_count"]})
    except PDFProcessingError as e:
        logger.exception(f"Error processing document {document_id}")
        return APIResponse(success=False, message="Failed to process the file.", data=None)
    except Exception as e:
        logger.exception(f"Unexpected error processing document {document_id}")
        return APIResponse(success=False, message="Unexpected error occurred while processing the file.", data=None)




    

from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
from pathlib import Path
from app.models.api_response import APIResponse
from app.utils.logger import get_logger
from app.config.settings import settings

logger = get_logger(__name__)

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    
    if not file.filename:
        logger.warning("Upload attempt without a filename.")
        return APIResponse(success=False, message="No file provided", data=None)

    
    extension = Path(file.filename).suffix.lower()
    if extension != ".pdf":
        logger.warning(f"Invalid file format uploaded: {extension}")
        return APIResponse(success=False, message="Invalid file format. Only PDF files are allowed", data=None)

    
    if file.size and file.size > 5 * 1024 * 1024:
        logger.warning(f"File size {file.size} exceeds the 5MB limit.")
        return APIResponse(success=False, message="File size exceeds the limit of 5MB", data=None)


    document_id = str(uuid4())
    stored_filename = f"{document_id}{extension}"
    upload_dir = settings.base_dir / "data" / "documents"
    upload_dir.mkdir(parents=True, exist_ok=True)
    filepath = upload_dir / stored_filename
    
    try:
        content = await file.read()
        with filepath.open("wb") as f:
            f.write(content)
            
        logger.info(f"Document uploaded successfully: {stored_filename}")
        return APIResponse(
            success=True, 
            message="Document uploaded successfully", 
            data={
                "document_id": document_id,
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": file.size,
                "stored_filename": stored_filename
            }
        )

    except Exception as e:
        logger.exception("Error uploading document")
        return APIResponse(success=False, message="Failed to upload document", data=None)







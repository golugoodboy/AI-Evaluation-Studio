from fastapi import APIRouter, UploadFile, File
from uuid import uuid4
from pathlib import Path
from app.models.api_response import APIResponse
from app.utils.logger import get_logger
from app.config.settings import settings

from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.services.embeddings_services import EmbeddingsService
from app.services.document_storage_service import DocumentStorageService
from app.services.document_preprocessorv2 import DocumentProcessor
from app.services.vector_store.chromDBservice import ChromaDBService
import chromadb

logger = get_logger(__name__)

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_document(file: UploadFile = File(...), collection : str = None):
    if not file.filename:
        logger.warning("Upload attempt without a filename.")
        return APIResponse(success=False, message="No file provided", data=None)

    extension = Path(file.filename).suffix.lower()
    if extension != ".pdf":
        logger.warning(f"Invalid file format uploaded: {extension}")
        return APIResponse(success=False, message="Invalid file format. Only PDF files are allowed", data=None)

    # FastAPI's UploadFile does not provide a size attribute.
    # Read the file content and enforce a size limit manually.
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        logger.warning(f"File size {len(content)} exceeds the 5MB limit.")
        return APIResponse(success=False, message="File size exceeds the limit of 5MB", data=None)

    # Generate a UUID for the document and store the file
    document_id = str(uuid4())
    stored_filename = f"{document_id}{extension}"
    upload_dir = settings.base_dir / "data" / "documents"
    upload_dir.mkdir(parents=True, exist_ok=True)
    filepath = upload_dir / stored_filename

    try:
        # Write the uploaded file to disk
        with filepath.open("wb") as f:
            f.write(content)
        logger.info(f"Document uploaded successfully: {stored_filename}")

        # Process the PDF: extract, chunk, embed, and store metadata
        pdf_service = PDFService()
        chunk_service = ChunkService()
        embedding_service = EmbeddingsService()
        storage_service = DocumentStorageService()
        client = chromadb.PersistentClient(path=settings.base_dir / "data" / "chromadb")
        chromadb_service = ChromaDBService(client)
        processor = DocumentProcessor(pdf_service, chunk_service, embedding_service, storage_service,chromadb_service)
        processor.process_document(filepath, document_id=document_id, collection = collection)

        return APIResponse(
            success=True,
            message="Document uploaded and processed successfully",
            data={
                "document_id": document_id,
                "filename": file.filename,
                "content_type": file.content_type,
                "file_size": len(content),
                "stored_filename": stored_filename,
            },
        )
    except Exception as e:
        logger.exception("Error uploading or processing document")
        return APIResponse(success=False, message="Failed to upload document", data=None)


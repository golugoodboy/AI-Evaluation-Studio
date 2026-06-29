from fastapi import APIRouter
from app.utils.logger import get_logger
from app.models.api_response import APIResponse
from app.models.api_response import RAGRequest
from app.services.rag_service import RAGService
from app.services.embeddings_services import EmbeddingsService
from app.services.document_storage_service import DocumentStorageService
from app.services.llm.llm_service import LLMService
from app.services.retriever_services import RetrieverService
from app.services.llm.huggingface_provider import HuggingFaceProvider
logger = get_logger(__name__)
router = APIRouter(prefix="/rag", tags=["RAG"])


embedding_service = EmbeddingsService()

storage_service = DocumentStorageService()

retriever_service = RetrieverService()

provider = HuggingFaceProvider()

llm_service = LLMService(provider)

rag_service = RAGService(embedding_service,llm_service, retriever_service,storage_service)

@router.post("/")
def rag(request : RAGRequest):
    logger.info(f"Received request to rag: {request.document_id}")
    try:
        response = rag_service.process_query(
            query=request.query, 
            document_id=request.document_id
        )
        return APIResponse(success=True, message="Query processed successfully", data=response)
    except Exception as e:
        logger.exception(f"Error processing query {request.query}")
        return APIResponse(success=False, message=f"Failed to process the RAG: {str(e)} | Details: {error_details}", data=None)
    



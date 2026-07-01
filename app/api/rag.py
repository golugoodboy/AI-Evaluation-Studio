from fastapi import APIRouter
from app.utils.logger import get_logger
from app.models.api_response import APIResponse
from app.models.api_response import RAGRequest
from app.services.rag_service import RAGService
from app.services.embeddings_services import EmbeddingsService
#from app.services.document_storage_service import DocumentStorageService
from app.services.llm.llm_service import LLMService
from app.services.llm.huggingface_provider import HuggingFaceProvider
from app.services.retrieval_service.retrieverDBservice import RetrieverDBService
from app.config.settings import settings
import chromadb
from app.services.vector_store.chromDBservice import ChromaDBService

logger = get_logger(__name__)
router = APIRouter(prefix="/rag", tags=["RAG"])


embedding_service = EmbeddingsService()

#storage_service = DocumentStorageService()

client = chromadb.PersistentClient(path=settings.base_dir / "data" / "chromadb")
chromadb_service = ChromaDBService(client)
retriever_service = RetrieverDBService(chromadb_service)

provider = HuggingFaceProvider()

llm_service = LLMService(provider)

rag_service = RAGService(embedding_service,llm_service, retriever_service)


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
        return APIResponse(success=False, message = str(e), data = None)
    




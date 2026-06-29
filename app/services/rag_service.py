from app.utils.logger import get_logger
from app.services.embeddings_services import EmbeddingsService
from app.services.document_storage_service import DocumentStorageService
from app.services.llm.llm_service import LLMService
from app.services.retriever_services import RetrieverService
from typing import Dict, Any
from app.exceptions.pdf_exception import RAGProcessingError
from prompt.rag_prompt import RAGPrompt


logger = get_logger(__name__)

class RAGService:
    def __init__(self, embedding_service: EmbeddingsService, llm_service: LLMService, retriever_service: RetrieverService, document_storage_service: DocumentStorageService):
        self._embedding_service = embedding_service
        self._llm_service = llm_service
        self._retriever_service = retriever_service
        self._document_storage_service = document_storage_service
    
    def process_query(self, query : str, document_id : str, top_k : int = 3) -> Dict[str, Any]:
        logger.info(f"Processing query: {query}")
        try:
            document = self._document_storage_service.load_document(document_id)
            query_embedding = self._embedding_service.generate(query)
            retrieved_chunks = self._retriever_service.retrieve(query_embedding, document["embeddings_chunks"], top_k)
            rag_context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
            prompt = RAGPrompt.build(query, rag_context)
            response = self._llm_service.generate(prompt)
            return {
                "query": query,
                "retrieved_chunks": retrieved_chunks,
                "rag_context": rag_context,
                "response": response,
                "retrieval_count" : len(retrieved_chunks),
                "top_score" : (retrieved_chunks[0]["score"]) if retrieved_chunks else None,
                "prompt_version": RAGPrompt.PROMPT_VERSION
            }
        except Exception as e:
            logger.exception("Error processing query")
            raise RAGProcessingError("Failed to process query") from e



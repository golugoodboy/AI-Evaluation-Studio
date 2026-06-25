from app.utils.logger import get_logger
from app.services.embeddings_services import EmbeddingsService
from app.services.llm.llm_service import LLMService
from app.services.retriever_services import RetrieverService
from typing import List, Dict, Any
from app.exceptions.pdf_exception import RetrieveProcessingError,LLMProcessingError,RAGProcessingError


logger = get_logger(__name__)

class RAGService:
    def __init__(self, embedding_service: EmbeddingsService, llm_service: LLMService, retriever_service: RetrieverService):
        self._embedding_service = embedding_service
        self._llm_service = llm_service
        self._retriever_service = retriever_service
    
    def process_query(self, query : str, chunks : List[Dict[str, Any]], top_k : int = 3) -> Dict[str, Any]:
        logger.info(f"Processing query: {query}")
        try:
            query_embedding = self._embedding_service.generate(query)
            retrieved_chunks = self._retriever_service.retrieve(query_embedding, chunks, top_k)
            rag_context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
            prompt = f"Context: {rag_context}\n\nQuery: {query}\n\nAnswer:"
            response = self._llm_service.generate(prompt)
            return {
                "query": query,
                "retrieved_chunks": retrieved_chunks,
                "rag_context": rag_context,
                "response": response,
                "retrieval_count" : len(retrieved_chunks),
                "top_score" : retrieved_chunks[0]["score"]
            }
        except Exception as e:
            logger.exception("Error processing query")
            raise RAGProcessingError("Failed to process query") from e


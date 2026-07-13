from app.utils.logger import get_logger
from app.services.embeddings_services import EmbeddingsService
from app.services.llm.llm_service import LLMService
from typing import Dict, Any, Optional
from app.exceptions.pdf_exception import RAGProcessingError
from prompt.rag_promptv3 import RAGPrompt
from app.config.settings import settings
from app.services.retrieval_service.retrieverDBservicev2 import RetrieverDBService
from app.services.evaluation.evaluation_service import EvaluationService



logger = get_logger(__name__)

class RAGService:
    def __init__(self, embedding_service: EmbeddingsService, llm_service: LLMService, retriever_service: RetrieverDBService):
        self._embedding_service = embedding_service
        self._llm_service = llm_service
        self._retriever_service = retriever_service

    
    def process_query(self, query : str, top_k : int = 3, metadata_filter : Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        logger.info(f"Processing query: {query}")
        try:
            query_embedding = self._embedding_service.generate(query)
            retrieved_chunks = self._retriever_service.retrieve_chunks(query_embedding, top_k, metadata_filter)
            top_score = retrieved_chunks[0]["distance"] if retrieved_chunks else 0
            threshold = settings.rag_threshold
            if top_score < threshold:
                logger.warning(f"Top score {top_score} is below threshold {threshold}")
                return {
                    "query": query,
                    "retrieved_chunks": retrieved_chunks,
                    "rag_context": "I couldn't find the answer in the provided document.",
                    "response": "I couldn't find the answer in the provided document.",
                    "retrieval_count" : len(retrieved_chunks),
                    "distance" : (retrieved_chunks[0]["distance"]) if retrieved_chunks else None,
                }
            rag_context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
            prompt = RAGPrompt.build(query, rag_context)
            response = self._llm_service.generate(prompt)
            metrics = EvaluationService.generate_metrics(retrieved_chunks = retrieved_chunks, llm_response = response, prompt_version = RAGPrompt.PROMPT_VERSION)
            return {
                "query": query,
                "retrieved_chunks": retrieved_chunks,
                "rag_context": rag_context,
                "response": response,
                "retrieval_count" : len(retrieved_chunks),
                "distance" : (retrieved_chunks[0]["distance"]) if retrieved_chunks else None,
                "prompt_version": RAGPrompt.PROMPT_VERSION,
                "metrics" : metrics
            }
        except Exception as e:
            logger.exception("Error processing query")
            raise 






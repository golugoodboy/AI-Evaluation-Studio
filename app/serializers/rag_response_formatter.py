from app.utils.logger import get_logger
from typing import Dict, Any
logger = get_logger(__name__)

class RAGResponseFormatter:
    @staticmethod
    def format_rag_response_debug(response : Dict[str, Any]) -> Dict[str, Any]:
        return response
    
    @staticmethod
    def format_rag_response_production(response: Dict[str, Any]) -> Dict[str,Any]:
        answer = response["response"]
        chunks_list = response["retrieved_chunks"]
        sources = [{
            "chunk_id" : res["id"],
            "rank" : res["rank"],
            "distance" : res["distance"],
        } for res in chunks_list]

        return {
            "answer" : answer,
            "sources" : sources
        }









    



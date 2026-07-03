from app.utils.logger import get_logger
from typing import Dict, Any, List



logger = get_logger(__name__)

class EvaluationService:
    @staticmethod
    def generate_metrics(retrieved_chunks : List[Dict[str, Any]], llm_response : Dict[str, Any], prompt_version :str):
        chunks = retrieved_chunks
        distances = [chunk["distance"] for chunk in chunks]
        if distances:
            average_distance = sum(distances)/len(distances)
            max_distance = max(distances)
            min_distance = min(distances)
        else:
            average_distance = 0
            max_distance = 0
            min_distance = 0
        retrieval_success = len(chunks) > 0
        metrics ={
            "prompt_version" : prompt_version,
            "retrieval_success" : retrieval_success,
            "retrieval_metrics" : {
                "average_distance" : average_distance,
                "max_distance" : max_distance,
                "min_distance" : min_distance
            },
            "llm_metrics" : {
                "latency" : llm_response["latency"],
                "tokens_used" : llm_response["tokens_used"],
                "model_used" : llm_response["model"],
                "provider" : llm_response["provider"]
            }
        }
        logger.info("Evaluation Metrics Generated Successfully.")
        return metrics





        
    





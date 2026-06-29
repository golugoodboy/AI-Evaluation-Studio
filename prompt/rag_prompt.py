from typing import List, Dict, Any
from app.utils.logger import get_logger

logger = get_logger(__name__)

class RAGPrompt:
    PROMPT_VERSION = "1.0"
    @staticmethod
    def build(question : str, context : str) -> str:
        prompt = f"""
        You are an AI assistant that answers the questions ONLY using the provided context.
        If the answer cannot be found in the context, just say : I couldn't find the answer in the given document.
        Do not make up information.
        
        Context :
        ---------------------------------- 
        {context}
        ----------------------------------
        
        Question :
        {question}
        ----------------------------------
        Provide a clear and concise answer based only on the context above.
        """
        return prompt


        
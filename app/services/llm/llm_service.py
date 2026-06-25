from app.services.llm.basellmprovider import BaseLLMProvider
from app.utils.logger import get_logger

logger = get_logger(__name__)

class LLMService:
    def __init__(self, provider : BaseLLMProvider):
        self._provider = provider
    
    def generate(self, prompt : str) -> dict:
        return self._provider.generate(prompt)
    


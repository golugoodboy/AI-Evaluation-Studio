from app.utils.logger import get_logger
from app.config.settings import settings

logger = get_logger(__name__)

class BaseLLMProvider:
    def __init__(self, model_name : str):
        self._model_name = model_name
        self.api_key = settings.huggingface_api_key

    def generate(self, prompt : str) -> dict:
        raise NotImplementedError("You must implement the generate method.")






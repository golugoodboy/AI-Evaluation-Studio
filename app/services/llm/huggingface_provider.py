from app.utils.logger import get_logger
from app.services.llm.basellmprovider import BaseLLMProvider
from app.exceptions.pdf_exception import LLMProcessingError
from app.config.settings import settings
from huggingface_hub import InferenceClient
import time


logger = get_logger(__name__)

class HuggingFaceProvider(BaseLLMProvider):
    def __init__(self, model_name : str | None = None):
        chosen_model = model_name or settings.huggingface_model
        if not chosen_model:
            raise ValueError("Model name is required.")
        super().__init__(chosen_model)
        self._model_name = chosen_model
        try:
            self._client = InferenceClient(api_key = settings.huggingface_api_key)
            logger.info(f"Hugging Face provider Initialized with name : {self._model_name}")
        except Exception as e:
            logger.exception("Error initializing HuggingFace provider")
            raise LLMProcessingError("Failed to initialize HuggingFace provider") from e

    def generate(self, prompt : str) -> dict:
        logger.info("Sending request to Hugging Face.")
        start = time.perf_counter()
        try:
            response = self._client.chat_completion(
                messages = [{"role": "user", "content": prompt}],
                model = self._model_name,
                max_tokens = 512,
                temperature = 0.5
            )
            
            output_text = response.choices[0].message.content
            latency = round((time.perf_counter() - start) * 1000, 2)
            logger.info(f"Successfully received response from Hugging Face provider in {latency} ms")
            
            prompt_tokens = response.usage.prompt_tokens if hasattr(response, 'usage') and response.usage else 0
            completion_tokens = response.usage.completion_tokens if hasattr(response, 'usage') and response.usage else 0
            total_tokens = response.usage.total_tokens if hasattr(response, 'usage') and response.usage else 0
            finish_reason = response.choices[0].finish_reason if len(response.choices) > 0 else None

            return {
                "text" : output_text,
                "latency" : latency,
                "model" : self._model_name,
                "provider" : "HuggingFace",
                "tokens_used" : total_tokens,
                "usage":{
                    "prompt_tokens" : prompt_tokens,
                    "response_tokens" : completion_tokens,
                    "total_tokens" : total_tokens
                },
                "finish_reason": finish_reason
            }
        except Exception as e:
            logger.exception("Error generating response from HuggingFace provider")
            raise LLMProcessingError("Failed to generate response from HuggingFace provider") from e


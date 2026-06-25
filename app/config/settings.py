from dotenv import load_dotenv
from pathlib import Path
import os


def get_base_path():
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if(parent / ".env").exists():
            return parent
    
    return current_path.parent


base_dir = get_base_path()
load_dotenv(dotenv_path = base_dir / ".env")

class Settings:
    def __init__(self):
        self.base_dir = base_dir
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.app_name = os.getenv("APP_NAME")
        self.app_version = os.getenv("APP_VERSION")
        self.app_environment = os.getenv("ENVIRONMENT")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.huggingface_model = os.getenv("HUGGINGFACE_MODEL")



settings = Settings()


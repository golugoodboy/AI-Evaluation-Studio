from typing import Any
from pydantic import BaseModel
from app.config.settings import settings

class APIResponse(BaseModel):
    success : bool
    message : str
    data : Any | None = None
    version : str = settings.app_version





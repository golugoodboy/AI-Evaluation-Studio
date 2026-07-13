from typing import Any, Dict, Optional
from pydantic import BaseModel
from app.config.settings import settings

class APIResponse(BaseModel):
    success : bool
    message : str
    data : Any | None = None
    version : str = settings.app_version


class RAGRequest(BaseModel):
    query : str
    metadata_filter : Optional[Dict[str, Any]] = None








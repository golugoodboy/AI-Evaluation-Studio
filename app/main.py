from fastapi import FastAPI
from app.config.settings import settings
from app.utils.logger import get_logger
from app.models.api_response import APIResponse
from app.api.routes import router
from app.api import upload,process

logger = get_logger(__name__)
logger.info("API Starting...")


app = FastAPI(
    title = settings.app_name,
    version = settings.app_version,
    description = "AI Evaluation Studio"
)

app.state.environment = settings.app_environment

app.include_router(router)
app.include_router(upload.router)
app.include_router(process.router)










from fastapi import FastAPI
from app.config.settings import settings
from app.utils.logger import get_logger
from app.models.api_response import APIResponse

logger = get_logger(__name__)
logger.info("API Starting...")


app = FastAPI(
    title = settings.app_name,
    version = settings.app_version,
    description = "AI Evaluation Studio"
)

app.state.environment = settings.app_environment


@app.get("/")
async def home():
    logger.info("Home Endpoint Called.")
    return APIResponse(
        success = True,
        message = "Welcome to AI Evaluation Studio",
        data = {
            "app_name" : settings.app_name,
            "app_version" : settings.app_version,
            "app_environment" : settings.app_environment
        },
        version = settings.app_version
    )








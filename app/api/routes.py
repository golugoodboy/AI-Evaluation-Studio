from fastapi import APIRouter
from app.utils.logger import get_logger
from app.models.api_response import APIResponse
from app.config.settings import settings



logger = get_logger(__name__)
router = APIRouter()

@router.get("/")
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

@router.get("/health")
async def health_check():
    logger.info("Health Check Requested.")
    return APIResponse(
        success = True,
        message = "Application is Healthy.",
        data = {
            "app_name" : settings.app_name,
            "app_version" : settings.app_version,
            "app_environment" : settings.app_environment
        },
        version = settings.app_version
    )






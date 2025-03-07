from fastapi import FastAPI
from health_app.core.config import settings
from health_app.backend.api.api_v1.api_router import router

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.include_router(router, prefix=settings.API_V1_STR)
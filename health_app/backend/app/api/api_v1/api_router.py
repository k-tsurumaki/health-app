from fastapi import APIRouter

from health_app.backend.app.api.api_v1.endpoints import meals, users, weight_records

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(meals.router, prefix="/meals", tags=["meals"])
router.include_router(weight_records.router, prefix="/weight_records", tags=["weight_records"])
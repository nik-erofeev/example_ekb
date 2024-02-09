"""Корневой роутер приложения"""

from fastapi import APIRouter

from app.api.codes.router import router as products_router
from app.api.shift_tasks.router import router as shift_tasks_router
from app.config import settings


router = APIRouter(prefix=settings.api_v1_prefix)

routers = (
    shift_tasks_router,
    products_router,
)


for resource_router in routers:
    router.include_router(resource_router)

"""Корневой роутер приложения"""

from fastapi import APIRouter

from app.api.test_router_api.router import router as test_router
from app.config import settings


router = APIRouter(prefix=settings.api_v1_prefix)

routers = (test_router,)


for resource_router in routers:
    router.include_router(resource_router)

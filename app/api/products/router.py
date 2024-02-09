from fastapi import APIRouter, status

from app.api.products.schemas import CodeResponseSchemas
from app.api.products.services import CodeService


router = APIRouter(
    prefix="/codes",
    tags=["Уникальные Коды"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=list[CodeResponseSchemas],
)
async def create_unique_codes(codes: CodeService.create_dep):
    return codes

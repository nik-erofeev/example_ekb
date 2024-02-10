from fastapi import APIRouter, status

from app.api.codes.schemas import CodeResponseSchemas
from app.api.codes.services import CodeService


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


@router.patch(
    "/{code_id}",
    status_code=status.HTTP_200_OK,
    response_model=CodeResponseSchemas,
)
async def aggregated(aggregate: CodeService.aggregate_codes_dep):
    return aggregate

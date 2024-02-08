from fastapi import APIRouter


router = APIRouter(
    prefix="/test_router_api",
    tags=["test_router_api"],
)


@router.get("/")
async def get_test():
    return {"test_router_api": "ok"}

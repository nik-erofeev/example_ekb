from fastapi import HTTPException
from starlette import status


http_code_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Уникальный Код Продукта уже существует",
)

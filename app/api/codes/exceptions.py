from fastapi import HTTPException, status


http_not_found_code_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Продукции с данным уникальным кодом не существует",
)

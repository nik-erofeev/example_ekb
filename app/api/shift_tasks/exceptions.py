from fastapi import HTTPException, status


http_data_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с такой партией уже существует",
)


http_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Сменное задание не найдено",
)

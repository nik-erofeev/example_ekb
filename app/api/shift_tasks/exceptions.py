from fastapi import HTTPException, status


http_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Сменное задание не найдено",
)


http_date_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Не корректные ДатаПартии и Номер Партии",
)

http_edit_conflict_exception = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Данные для обновления не представлены",
)

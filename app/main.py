from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from sqlalchemy.exc import NoResultFound

from app.exceptions import sqlalchemy_not_found_exception_handler
from app.router import router


app = FastAPI(
    title="Контроль заданий на выпуск продукции",
    description="Получать сменные задания (партии) и уникальные идентификаторы продукции в рамках этой партии",  # noqa
    version="1.0.0",
)


app.include_router(router)
app.add_exception_handler(
    NoResultFound,
    sqlalchemy_not_found_exception_handler,
)
app.add_exception_handler(
    ResponseValidationError,
    sqlalchemy_not_found_exception_handler,
)

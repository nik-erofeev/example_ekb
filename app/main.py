from fastapi import FastAPI

from app.router import router


app = FastAPI(
    title="Контроль заданий на выпуск продукции",
    description="Получать сменные задания (партии) и уникальные идентификаторы продукции в рамках этой партии",  # noqa
    version="1.0.0",
)


app.include_router(router)

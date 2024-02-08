from fastapi.responses import JSONResponse


def sqlalchemy_not_found_exception_handler(*_):
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Ресурс не найден",
        },
    )

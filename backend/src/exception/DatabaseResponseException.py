from fastapi import Request
from fastapi.responses import JSONResponse
import logging


logger = logging.getLogger("database_exception_handler")

class DatabaseResponseException(Exception):
    """Обработчик ошибок, возникающих при обращении к базе данных."""
    def __init__(self, error: str =''):
        self.message = f"ошибка при обращении к базе данных: {error}"
        super().__init__(self.message)


async def database_response_exception_handler(request: Request, exc: DatabaseResponseException):
    logger.exception(f"ошибка при обращении к базе данных {request.url}: {exc.message}")
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message}
    )
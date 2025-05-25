from fastapi import Request
from fastapi.responses import JSONResponse
import logging


logger = logging.getLogger("serve_validation_error_exception_handler")

class ServerValidationException(Exception):
    """обработчик исключений возникающих при ошибки валидации на сервере"""
    def __init__(self, error: str =''):
        self.message = f"Ошибка валидации на сервере: {error}"
        super().__init__(self.message)


async def server_validation_exception_handler(request: Request, exc: ServerValidationException):
    logger.exception(f"ошибка на сервере {request.url}: {exc.message}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.message}
    )

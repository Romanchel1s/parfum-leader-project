from fastapi import Request
from fastapi.responses import JSONResponse
import logging


logger = logging.getLogger("exception_handler")

class CustomException(Exception):
    """Любая отдельно неучтенная ошибка"""
    def __init__(self, error: str =''):
        self.message = f"{error}"
        super().__init__(self.message)


async def custom_exception_handler(request: Request, exc: CustomException):
    logger.exception(f"ошибка {request.url}: {exc.message}")
    return JSONResponse(
        status_code=500,
        content={"detail": exc.message}
    )

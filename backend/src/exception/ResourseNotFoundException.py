from fastapi import Request
from fastapi.responses import JSONResponse
import logging


logger = logging.getLogger("resourse_not_exception_handler")

class ResourceNotFoundException(Exception):
    """Обработчик ошибок, возникающих при отсутствии указанного ресурса"""
    def __init__(self, error: str = ""):
        self.message = f"{error}"
        super().__init__(self.message)


async def resourse_not_found_exception_handler(request: Request, exc: ResourceNotFoundException):
    logger.exception(f"ошибка при обращении к ресурсу {request.url}: {exc.message}")
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message}
    )
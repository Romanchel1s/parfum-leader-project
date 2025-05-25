from dependency_injector.containers import DeclarativeContainer
from pydantic_settings import BaseSettings
from fastapi import FastAPI
import uvicorn
import asyncio
import logging
from fastapi.middleware.cors import CORSMiddleware

from config import Settings

from src.init_container import init_container

from src.router.store_router import store_router
from src.router.employee_router import employee_router
from src.router.product_router import product_router

from src.exception.DatabaseResponseException import DatabaseResponseException, database_response_exception_handler
from src.exception.ServerValidationException import ServerValidationException, server_validation_exception_handler
from src.exception.ResourseNotFoundException import ResourceNotFoundException, resourse_not_found_exception_handler
from src.exception.CustomException import CustomException, custom_exception_handler


async def fastapi_app(container: DeclarativeContainer, settings: BaseSettings):
    """
    Создает и запускает FastAPI приложение с подключением маршрутов и обработчиков исключений.
    
    :param container: Контейнер зависимостей, предоставляющий сервисы и репозитории.
    :param settings: Настройки приложения, включая параметры для запуска сервера.
    """
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"], 
        )

    # Подключаем роутеры для работы с магазинами и сотрудниками
    app.include_router(store_router(container))
    app.include_router(employee_router(container))
    app.include_router(product_router(container))

    # Добавляем обработчики исключений для кастомных исключений
    app.add_exception_handler(DatabaseResponseException, database_response_exception_handler)
    app.add_exception_handler(ServerValidationException, server_validation_exception_handler)
    app.add_exception_handler(ResourceNotFoundException, resourse_not_found_exception_handler)

    app.add_exception_handler(CustomException, custom_exception_handler)

    # Настройка и запуск Uvicorn сервера
    config = uvicorn.Config(
        app,
        reload=True,
        host=settings.run.host,
        port=settings.run.port,
    )
    server = uvicorn.Server(config=config)

    # Асинхронный запуск сервера
    await server.serve()


if __name__ == '__main__':
    # Настройка логирования в файл
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("app.log", mode='a', encoding='utf-8'),
        ]
    )
    logger = logging.getLogger("main")
    logger.info("Запуск программы")

    # Инициализация настроек и контейнера зависимостей
    settings: BaseSettings = Settings()
    container: DeclarativeContainer = init_container(settings)
    
    # Запуск приложения
    asyncio.run(fastapi_app(container, settings))

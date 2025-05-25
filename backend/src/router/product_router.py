from dependency_injector.containers import DeclarativeContainer
from fastapi import APIRouter, Path
from typing import List

from src.schema.product_schema import Product

from src.service.IService import IService


def product_router(container: DeclarativeContainer) -> APIRouter:
    """
    Создает маршрутизатор для работы с продуктами.
    
    Параметры:
    - container: DeclarativeContainer - Контейнер зависимостей, используемый для получения сервисов
      для получения информации о продуктах.
    
    Возвращает:
    - APIRouter: Маршрутизатор с конечными точками для работы с продуктами.
    """
    router = APIRouter(prefix='/product', tags=['product'])

    get_all_product_service: IService = container.get_all_product_service()
    get_product_service: IService = container.get_product_service()


    @router.get("/all_products", response_model=List[Product])
    async def get_all_product() -> List[Product]:
        """
        Получает список всех продуктов.

        Возвращает:
        - List[Product]: Список всех продуктов.
        """
        return await get_all_product_service.execute()

    @router.get("/{prod_id}", response_model=Product)
    async def get_product(
            prod_id: str = Path(..., description="ID товара"),
    ) -> Product:
        """
        Получает информацию о продукте по его ID.
        
        Параметры:
        - prod_id: str - Идентификатор продукта.
        
        Возвращает:
        - Product: Информация о продукте.
        """
        return await get_product_service.execute(prod_id)
    
    return router

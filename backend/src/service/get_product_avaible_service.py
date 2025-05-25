from pydantic import ValidationError
from typing import List

from src.schema.product_avaible_schema import ProductAvailable

from src.repository.interfaces.IStores_repository import IStoreRepository

from src.service.IService import IService

from src.exception.CustomException import CustomException
from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException


class GetProductAvailable(IService[List[ProductAvailable]]):
    """
    Сервис для получения информации о наличии товара в магазине.
    
    В случае ошибок выбрасывает исключения:
    - ResourceNotFoundException, если магазин не найден или отсутствует информация по товару.
    - ServerValidationException, если произошла ошибка валидации данных.
    - CustomException, если произошла неизвестная ошибка.
    """
    def __init__(self, repository: IStoreRepository):
        """
        Инициализирует сервис с переданным репозиторием магазинов.
        
        Параметры:
        - repository: Репозиторий магазинов, реализующий интерфейс IStoreRepository.
        """
        self.repository = repository

    async def execute(self, store_id: int, prod_id: str) -> List[ProductAvailable]:
        """
        Получает информацию о наличии товара в магазине по указанным параметрам.

        Параметры:
        - store_id: Идентификатор магазина.
        - prod_id: Идентификатор товара.
        
        Возвращает:
        - Список объектов ProductAvailable с информацией о наличии товара.
        
        Исключения:
        - ResourceNotFoundException: Если магазин не найден или нет данных о товаре.
        - ServerValidationException: Ошибка при валидации данных.
        - CustomException: Прочие ошибки.
        """
        product_avaible_data = await self.repository.get_product_available(store_id, prod_id)
        
        if not product_avaible_data:
            raise ResourceNotFoundException(f'магазин {store_id} не найден или нет информации по данному товару: {prod_id}')
        
        try:
            avaible = []

            for data in product_avaible_data:
                avaible.append(ProductAvailable(**data))

            return avaible
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e)
        
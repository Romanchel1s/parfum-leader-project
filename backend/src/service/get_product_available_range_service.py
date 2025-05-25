from pydantic import ValidationError
from typing import List
from datetime import datetime

from src.schema.product_avaible_schema import ProductAvailable

from src.repository.interfaces.IStores_repository import IStoreRepository

from src.service.IService import IService

from src.exception.CustomException import CustomException
from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException



class GetProductAvailableRange(IService[List[ProductAvailable]]):
    """
    Сервис для получения информации о наличии товаров в магазине за заданный временной промежуток.
    
    В случае ошибок выбрасывает исключения:
    - ResourceNotFoundException, если магазин не найден или отсутствует информация по товарам.
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

    async def execute(self, store_id: int, start_time: datetime, end_time: datetime) -> List[ProductAvailable]:
        """
        Получает информацию о наличии товаров в магазине в пределах заданного временного промежутка.

        Параметры:
        - store_id: Идентификатор магазина.
        - start_time: Начало временного промежутка.
        - end_time: Конец временного промежутка.
        
        Возвращает:
        - Список объектов ProductAvailable с информацией о наличии товаров в указанный период.
        
        Исключения:
        - ResourceNotFoundException: Если магазин не найден или нет данных о товарах.
        - ServerValidationException: Ошибка при валидации данных.
        - CustomException: Прочие ошибки.
        """
        product_avaible_data = await self.repository.get_product_available_range(store_id, start_time, end_time)
        
        if not product_avaible_data:
            raise ResourceNotFoundException(f'магазин {store_id} не найден или нет информации по товарам')
        
        try:
            avaible = []

            for data in product_avaible_data:
                avaible.append(ProductAvailable(**data))

            return avaible
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e)
        
from typing import List
from pydantic import ValidationError

from src.service.IService import IService

from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException
from src.exception.CustomException import CustomException

from src.schema.product_schema import Product


class GetAllProductService(IService[List[Product]]):
    """
    Сервис для получения всех товаров из репозитория и преобразования их в объекты Product.
    
    В случае ошибок выбрасывает соответствующие исключения, такие как ResourceNotFoundException,
    ServerValidationException или CustomException.
    """
    def __init__(self, repository):
        """
        Инициализирует сервис для получения всех товаров.
        
        Параметры:
        - repository: Репозиторий для работы с данными о товарах.
        """
        self.repository = repository

    async def execute(self) -> List[Product]:
        """
        Получает все товары из репозитория и преобразует их в объекты Product.
        
        Параметры:
        - нет
        
        Возвращает:
        - List[Product]: Список объектов Product, представляющих все товары.
        
        Исключения:
        - ResourceNotFoundException: Если товары не найдены.
        - ServerValidationException: Если произошла ошибка при валидации данных.
        - CustomException: Если произошла другая ошибка во время выполнения.
        """
        all_products = await self.repository.get_all_product()
        
        if not all_products:
            raise ResourceNotFoundException(f'Товары не найдены')
        
        try:
            products = []

            for data in all_products:
                products.append(Product(**data))

            return products
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e)
        
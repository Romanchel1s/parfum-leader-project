from pydantic import ValidationError

from src.schema.product_schema import Product

from src.repository.interfaces.IProduct_repository import IProductRepository

from src.service.IService import IService

from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException
from src.exception.CustomException import CustomException


class GetProductService(IService[Product]):
    """
    Сервис для получения информации о продукте по его ID.
    
    В случае ошибок выбрасывает исключения:
    - ResourceNotFoundException, если товар с заданным ID не найден.
    - ServerValidationException, если произошла ошибка валидации данных.
    - CustomException, если произошла неизвестная ошибка.
    """
    def __init__(self, repository: IProductRepository):
        """
        Инициализирует сервис с переданным репозиторием продуктов.
        
        Параметры:
        - repository: Репозиторий продуктов, реализующий интерфейс IProductRepository.
        """
        self.repository = repository

    async def execute(self, prod_id: str) -> Product:
        """
        Получает информацию о продукте по его ID.
        
        Параметры:
        - prod_id: Идентификатор продукта.
        
        Возвращает:
        - Объект Product с информацией о продукте.
        
        Исключения:
        - ResourceNotFoundException: Если товар с заданным ID не найден.
        - ServerValidationException: Ошибка при валидации данных.
        - CustomException: Прочие ошибки.
        """
        product_data = await self.repository.get_product(prod_id)
        
        if not product_data:
            raise ResourceNotFoundException(f'Товар {prod_id} не найден')
        
        try:
            product = product_data[0]
            product = Product(**product)

            print(product)
            return product
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e)
        
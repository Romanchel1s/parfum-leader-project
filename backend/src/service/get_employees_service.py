from typing import List
from pydantic import ValidationError

from src.service.IService import IService
from src.schema.employee_schema import Employee
from src.repository.interfaces.IStores_repository import IStoreRepository

from src.exception.CustomException import CustomException
from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException


class GetEmployeesService(IService[List[Employee]]):
    """
    Сервис для получения списка сотрудников магазина по его ID.
    
    В случае ошибок выбрасывает исключения:
    - ResourceNotFoundException, если магазин не найден или в нем нет сотрудников.
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

    async def execute(self, store_id: int) -> List[Employee]:
        """
        Получает список сотрудников для указанного магазина.

        Параметры:
        - store_id: Идентификатор магазина.

        Возвращает:
        - Список сотрудников в виде объектов Employee.
        
        Исключения:
        - ResourceNotFoundException: Если магазин не найден или не содержит сотрудников.
        - ServerValidationException: Ошибка при валидации данных.
        - CustomException: Прочие ошибки.
        """
        employees_data = await self.repository.get_employees(store_id)
        
        if not employees_data:
            raise ResourceNotFoundException(f'Магазин {store_id} не найден или в нем отсутствуют сотрудники')
        
        try:
            employees = []

            for data in employees_data:
                employees.append(Employee(**data))

            return employees
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e)
        
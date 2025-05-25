from pydantic import ValidationError

from src.schema.nearest_schema import Nearest

from src.repository.interfaces.IEmployees_repository import IEmployeesRepository

from src.service.IService import IService

from src.exception.CustomException import CustomException
from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException


class GetNearestService(IService[Nearest]):
    """
    Сервис для получения ближайшего графика работы сотрудника по его ID.
    
    В случае ошибок выбрасывает исключения:
    - ResourceNotFoundException, если сотрудник не найден или для него отсутствует расписание.
    - ServerValidationException, если произошла ошибка валидации данных.
    - CustomException, если произошла неизвестная ошибка.
    """
    def __init__(self, repository: IEmployeesRepository):
        """
        Инициализирует сервис с переданным репозиторием сотрудников.
        
        Параметры:
        - repository: Репозиторий сотрудников, реализующий интерфейс IEmployeesRepository.
        """
        self.repository = repository

    async def execute(self, employee_id: int) -> Nearest:
        """
        Получает ближайшее расписание для указанного сотрудника.

        Параметры:
        - employee_id: Идентификатор сотрудника.
        
        Возвращает:
        - Объект Nearest с информацией о графике работы сотрудника.
        
        Исключения:
        - ResourceNotFoundException: Если сотрудник не найден или не имеет расписания.
        - ServerValidationException: Ошибка при валидации данных.
        - CustomException: Прочие ошибки.
        """
        nearest_data = await self.repository.get_nearest(employee_id)
        if not nearest_data:
            raise ResourceNotFoundException(f'Сотрудник {employee_id} не найден или для него отсутствует раписание')
        
        try:
            nearest = Nearest(**nearest_data[0])
            return nearest
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e)

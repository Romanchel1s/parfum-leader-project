from pydantic import ValidationError
from typing import List
from datetime import datetime

from src.schema.employee_attendance_schema import EmployeeAttendance

from src.repository.interfaces.IEmployees_repository import IEmployeesRepository

from src.service.IService import IService

from src.exception.CustomException import CustomException
from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException


class GetAttendanceService(IService[List[EmployeeAttendance]]):
    """
    Сервис для получения списка посещений сотрудника по его ID.
    
    В случае ошибок выбрасывает исключения:
    - ResourceNotFoundException, если данные о посещении не найдены.
    - ServerValidationException, если произошла ошибка валидации данных.
    - CustomException, если произошла неизвестная ошибка.
    """
    def __init__(self, repository: IEmployeesRepository):
        """
        Инициализирует сервис для получения посещений сотрудника.

        Параметры:
        - repository: Репозиторий для работы с данными о посещении сотрудников.
        """
        self.repository = repository

    async def execute(self, employee_id: int, start_time: datetime, end_time: datetime) -> List[EmployeeAttendance]:
        """
        Получает список посещений сотрудника.

        Параметры:
        - employee_id: Идентификатор сотрудника.
        - start_time: Начало временного промежутка.
        - end_time: Конец временного промежутка.

        Возвращает:
        - Список посещений сотрудника в виде объектов EmployeeAttendance.
        
        Исключения:
        - ResourceNotFoundException: Если посещения не найдены для сотрудника.
        - ServerValidationException: Ошибка при валидации данных.
        - CustomException: Прочие ошибки.
        """
        attendance_data = await self.repository.get_employee_attendance(employee_id, start_time, end_time)
        if not attendance_data:
            raise ResourceNotFoundException(f'Сотрудник {employee_id} не найден или для него отсутствует раписание')
        
        try: 
            attendance = []

            for data in attendance_data:
                attendance.append(EmployeeAttendance(**data))

            return attendance
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e)

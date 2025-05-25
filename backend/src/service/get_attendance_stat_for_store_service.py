from typing import List
from datetime import datetime
from pydantic import ValidationError

from src.schema.employee_attendance_stat_schema import EmployeeAttendanceStatByDate, EmployeeAttendanceShort

from src.repository.interfaces.IStores_repository import IStoreRepository

from src.service.IService import IService

from src.exception.CustomException import CustomException
from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException


class GetAttendanceStatForStoreService(IService[List[EmployeeAttendanceStatByDate]]):
    """
    Сервис для получения статистики посещаемости сотрудников по магазину за период.

    Параметры:
    - repository: IStoreRepository — репозиторий магазинов.

    Возвращает:
    - List[EmployeeAttendanceStatByDate]: список статистики по датам.
    """
    def __init__(self, repository: IStoreRepository):
        self.repository = repository

    async def execute(self, store_id: int, start_time: datetime, end_time: datetime) -> List[EmployeeAttendanceStatByDate]:
        """
        Получение статистики посещаемости сотрудников по магазину за период.

        Параметры:
        - store_id: int — идентификатор магазина.
        - start_time: datetime — начало диапазона.
        - end_time: datetime — конец диапазона.

        Возвращает:
        - List[EmployeeAttendanceStatByDate]: список статистики по датам.
        """
        try:
            data = await self.repository.get_attendance_stat_for_store(store_id, start_time, end_time)

            if not data:
                raise ResourceNotFoundException('Нет данных по посещаемости для этого магазина и периода')
            
            result = []

            for item in data:
                employees = [EmployeeAttendanceShort(**emp) for emp in item["employees"]]
                result.append(EmployeeAttendanceStatByDate(date=item["date"], employees=employees))

            return result
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e) 
        
from pydantic import ValidationError
from typing import List
from datetime import datetime

from src.schema.nearest_from_store import NearestFromStoreByDate, NearestFromStore

from src.repository.interfaces.IStores_repository import IStoreRepository

from src.service.IService import IService

from src.exception.CustomException import CustomException
from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException


class GetNearestFromStoreService(IService[List[NearestFromStoreByDate]]):
    """
    Сервис для получения информации о посещаемости сотрудников по магазинам за указанный период.

    Параметры:
    - repository: IStoreRepository — репозиторий магазинов.

    Возвращает:
    - List[NearestFromStoreByDate]: список объектов, где для каждой даты содержится список магазинов с количеством присутствующих и отсутствующих.
    """
    def __init__(self, repository: IStoreRepository):
        self.repository = repository

    async def execute(self, start_time: datetime, end_time: datetime) -> List[NearestFromStoreByDate]:
        """
        Получение информации о посещаемости сотрудников по магазинам за указанный период.

        Параметры:
        - start_time: datetime — начало временного диапазона.
        - end_time: datetime — конец временного диапазона.

        Возвращает:
        - List[NearestFromStoreByDate]: список с данными по датам, где каждая дата содержит список магазинов с количеством присутствующих и отсутствующих.
        """
        attendance_data = await self.repository.get_nearest_from_store(start_time, end_time)
        
        if not attendance_data:
            raise ResourceNotFoundException('магазины не найдены или нет информации по расписанию')
        
        try:
            result = []
            for date, stores_data in attendance_data.items():
                stores = [NearestFromStore(store_id=store_id, **attendance)
                          for store_id, attendance in stores_data.items()]
                result.append(NearestFromStoreByDate(date=date, stores=stores))
            return result
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e)
        
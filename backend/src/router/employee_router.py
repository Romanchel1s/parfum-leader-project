from dependency_injector.containers import DeclarativeContainer
from fastapi import APIRouter, Path
from typing import List
from datetime import datetime

from src.schema.nearest_schema import Nearest
from src.schema.employee_attendance_schema import EmployeeAttendance

from src.service.IService import IService


def employee_router(container: DeclarativeContainer) -> APIRouter:
    """
    Создает маршрутизатор для работы с конечными точками, связанными с сотрудниками.
    
    Параметры:
    - container: DeclarativeContainer - Контейнер зависимостей, используемый для получения сервисов, таких как
      поиск ближайшего сотрудника и информация о посещаемости сотрудника.
    
    Возвращает:
    - APIRouter: Маршрутизатор с конечными точками для работы с сотрудниками.
    """
    router = APIRouter(prefix='/employees', tags=['employees'])

    # Получаем сервисы из контейнера зависимостей
    get_nearest_service: IService = container.get_nearest_service()
    get_employee_attendance_service: IService = container.get_employee_attendance_service()


    @router.get("/{employee_id}/nearest", response_model=Nearest)
    async def get_employee_nearest(
            employee_id: int = Path(..., description="ID сотрудника", ge=1)
    ) -> Nearest:
        """
        Получает информацию о ближайшем графике работы для сотрудника по его ID.
        
        Параметры:
        - employee_id: int - Идентификатор сотрудника.
        
        Возвращает:
        - Nearest: Объект, содержащий информацию о ближайшем графике работы сотрудника.
        """
        return await get_nearest_service.execute(employee_id)
    
    @router.get("/{employee_id}/Attendance/{start_time}/{end_time}", response_model=List[EmployeeAttendance])
    async def get_employee_attendance(
            employee_id: int = Path(..., description="ID сотрудника", ge=1),
            start_time: datetime = Path(..., description="Начало диапазона"),
            end_time: datetime = Path(..., description="Конец диапазона"),
    ) -> List[EmployeeAttendance]:
        """
        Получает информацию о посещаемости сотрудника по его ID.
        
        Параметры:
        - employee_id: int - Идентификатор сотрудника.
        - start_time: datetime - начало временного диапазона.
        - end_time: datetime - конец временного диапазона.
        
        Возвращает:
        - List[EmployeeAttendance]: Список записей о посещаемости сотрудника за указанный период.
        """
        return await get_employee_attendance_service.execute(employee_id, start_time, end_time)
    
    return router

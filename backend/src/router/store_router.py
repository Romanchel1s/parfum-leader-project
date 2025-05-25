from dependency_injector.containers import DeclarativeContainer
from fastapi import APIRouter, Path, Body
from typing import List
from datetime import datetime

from src.schema.employee_schema import Employee
from src.schema.product_avaible_schema import ProductAvailable
from src.schema.nearest_from_store import NearestFromStoreByDate
from src.schema.employee_attendance_stat_schema import EmployeeAttendanceStatByDate
from src.schema.store_check_settings_update import StoreCheckSettingsUpdate

from src.service.IService import IService


def store_router(container: DeclarativeContainer) -> APIRouter:
    """
    Создание и возврат маршрутизатора для работы с магазинами.

    Параметры:
    - container: DeclarativeContainer — контейнер зависимостей, используемый для получения сервисов магазинов.

    Возвращает:
    - APIRouter: маршрутизатор FastAPI для работы с магазинами.
    """
    router = APIRouter(prefix='/stores', tags=['stores'])

    # Получение сервиса для работы с магазинами из контейнера зависимостей
    get_employees_sercice: IService = container.get_employees_service()
    get_product_available_service: IService = container.get_product_available_service()
    get_product_available_range_service: IService = container.get_product_available_range_service()
    get_nearest_from_store_service: IService = container.get_nearest_from_store_service()
    get_attendance_stat_for_store_service: IService = container.get_attendance_stat_for_store_service()
    update_store_check_settings_service: IService = container.update_store_check_settings_service()
    

    @router.get("/{store_id}/employees", response_model=List[Employee])
    async def get_store_employees(
            store_id: int = Path(..., description="ID магазина", ge=1)
    ) -> List[Employee]:
        """
        Получение списка сотрудников для указанного магазина по его ID.

        Параметры:
        - store_id: int — идентификатор магазина.

        Возвращает:
        - List[Employee]: список сотрудников магазина.
        """
        return await get_employees_sercice.execute(store_id)
    

    @router.get('/{store_id}/products/{prod_id}/products_available', response_model=List[ProductAvailable])
    async def get_product_available(
        store_id: int = Path(..., description="ID магазина", ge=1),
        prod_id: str = Path(..., description="ID товара"),
    ) -> List[ProductAvailable]:
        """
        Получение информации из Available для конкретного товара в указанном магазине.

        Параметры:
        - store_id: int — идентификатор магазина.
        - prod_id: str — идентификатор товара.

        Возвращает:
        - List[ProductAvailable]: список с данными из Available товара по магазинам.
        """
        return await get_product_available_service.execute(store_id, prod_id)


    @router.get('/{store_id}/products/products_available/{start_time}/{end_time}', response_model=List[ProductAvailable])
    async def get_product_available_range(
        store_id: int = Path(..., description="ID магазина", ge=1),
        start_time: datetime = Path(..., description="Начало диапазона"),
        end_time: datetime = Path(..., description="Конец диапазона"),
    ) -> List[ProductAvailable]:
        """
        Получение информации из Available для всех товаров в магазине за указанный период времени.

        Параметры:
        - store_id: int — идентификатор магазина.
        - start_time: datetime — начало временного диапазона.
        - end_time: datetime — конец временного диапазона.

        Возвращает:
        - List[ProductAvailable]: список с данными из Available за указанный период.
        """
        return await get_product_available_range_service.execute(store_id, start_time, end_time)

    @router.get('/nearest/{start_time}/{end_time}', response_model=List[NearestFromStoreByDate])
    async def get_nearest_from_store(
        start_time: datetime = Path(..., description="Начало диапазона"),
        end_time: datetime = Path(..., description="Конец диапазона"),
    ) -> List[NearestFromStoreByDate]:
        """
        Получение информации о посещаемости сотрудников по магазинам за указанный период.

        Параметры:
        - start_time: datetime — начало временного диапазона.
        - end_time: datetime — конец временного диапазона.

        Возвращает:
        - List[NearestFromStoreByDate]: список с данными по датам, где каждая дата содержит список магазинов с количеством присутствующих и отсутствующих.
        """
        return await get_nearest_from_store_service.execute(start_time, end_time)

    @router.get('/{store_id}/attendance_stat/{start_time}/{end_time}', response_model=List[EmployeeAttendanceStatByDate])
    async def get_attendance_stat_for_store(
        store_id: int = Path(..., description="ID магазина", ge=1),
        start_time: datetime = Path(..., description="Начало диапазона"),
        end_time: datetime = Path(..., description="Конец диапазона"),
    ) -> List[EmployeeAttendanceStatByDate]:
        """
        Получение статистики посещаемости сотрудников по магазину за указанный период.

        Параметры:
        - store_id: int — идентификатор магазина.
        - start_time: datetime — начало диапазона.
        - end_time: datetime — конец диапазона.

        Возвращает:
        - List[EmployeeAttendanceStatByDate]: список статистики по датам, где для каждой даты список сотрудников и их присутствие.
        """
        return await get_attendance_stat_for_store_service.execute(store_id, start_time, end_time)

    @router.put('/{store_id}/update_daily_checks', response_model=StoreCheckSettingsUpdate)
    async def update_store_check_settings(
        store_id: int = Path(..., description="ID магазина", ge=1),
        settings: StoreCheckSettingsUpdate = Body(...),
    ) -> StoreCheckSettingsUpdate:
        """
        Обновление настроек периодичности проверки товара для магазина.

        Параметры:
        - store_id: int — идентификатор магазина.
        - settings: StoreCheckSettingsUpdate — новые настройки.

        Возвращает:
        - StoreCheckSettingsUpdate: обновлённые настройки.
        """
        return await update_store_check_settings_service.execute(store_id, settings)

    return router

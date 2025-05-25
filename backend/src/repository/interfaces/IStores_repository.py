from abc import ABC, abstractmethod
from datetime import datetime


class IStoreRepository(ABC):
    """
    Абстрактный класс репозитория для работы с данными магазинов.
    
    Определяет методы для получения информации о сотрудниках магазина, наличии товаров и посещаемости.
    """
    
    @abstractmethod
    def __init__(self, session, *args):
        """
        Инициализирует репозиторий.
        
        Параметры:
        - session: объект сессии для работы с базой данных.
        - args: дополнительные аргументы, если требуется.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def get_employees(self, store_id: int):
        """
        Получение списка сотрудников магазина по его ID.
        
        Параметры:
        - store_id: int - идентификатор магазина.
        
        Возвращает:
        - Список сотрудников магазина в виде объектов Employee.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def get_product_available(self, store_id: int, prod_id: str):
        """
        Получение информации из Available конкретного товара в указанном магазине.
        
        Параметры:
        - store_id: int - идентификатор магазина.
        - prod_id: str - идентификатор товара.
        
        Возвращает:
        - Список объектов ProductAvailable с данными о наличии товара.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def get_product_available_range(self, store_id: int, date_start: datetime, date_end: datetime):
        """
        Получение информации из Available для товаров в магазине за указанный диапазон дат.
        
        Параметры:
        - store_id: int - идентификатор магазина.
        - date_start: datetime - начало временного диапазона.
        - date_end: datetime - конец временного диапазона.
        
        Возвращает:
        - Список объектов ProductAvailable с данными о наличии товаров за период.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def get_nearest_from_store(self, date_start: datetime, date_end: datetime):
        """
        Получение информации о посещаемости сотрудников по всем магазинам за указанный период.

        Параметры:
        - date_start: datetime — начало временного диапазона.
        - date_end: datetime — конец временного диапазона.

        Возвращает:
        - dict[str, dict[int, dict[str, int]]]:
            Словарь, где ключ первого уровня — дата (str),
            ключ второго уровня — ID магазина (int),
            значение — словарь с количеством присутствующих и отсутствующих ("present", "absent").
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def get_attendance_stat_for_store(self, store_id: int, date_start: datetime, date_end: datetime):
        """
        Получение статистики посещаемости сотрудников по магазину за указанный период.

        Параметры:
        - store_id: int — идентификатор магазина.
        - date_start: datetime — начало временного диапазона.
        - date_end: datetime — конец временного диапазона.

        Возвращает:
        - List[dict]: список словарей с ключами user_id, date, was_present.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def update_store_check_settings(self, store_id: int, daily_checks_count: int, daily_checks_interval: int):
        """
        Обновление настроек периодичности проверки товара для магазина.

        Параметры:
        - store_id: int — идентификатор магазина.
        - daily_checks_count: int — количество проверок в день.
        - daily_checks_interval: int — интервал между проверками.

        Возвращает:
        - dict: обновлённые данные магазина.
        """
        raise NotImplementedError()
    
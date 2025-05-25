from abc import ABC, abstractmethod


class IEmployeesRepository(ABC):
    """
    Абстрактный класс репозитория для работы с данными сотрудников.
    
    Определяет методы для получения информации о сотрудниках.
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
    async def get_nearest(self, employee_id: int):
        """
        Получение информации о графике сотруднике по его ID.
        
        Параметры:
        - employee_id: int - идентификатор сотрудника.
        
        Возвращает:
        - Объект Nearest с данными о графике сотрудника.
        """
        raise NotImplementedError()
    
    @abstractmethod
    async def get_employee_attendance(self, employee_id: int):
        """
        Получение данных о посещаемости сотрудника по его ID.

        Параметры:
        - employee_id: int - идентификатор сотрудника.

        Возвращает:
        - Объект или список с данными о посещаемости сотрудника.
        """
        raise NotImplementedError()
    
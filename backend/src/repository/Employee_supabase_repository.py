from supabase import Client
from datetime import datetime

from src.repository.interfaces.IEmployees_repository import IEmployeesRepository

from src.exception.DatabaseResponseException import DatabaseResponseException


class EmployeesSupabaseRepository(IEmployeesRepository):
    """
    Реализация репозитория для работы с данными сотрудников в базе данных Supabase.
    """
    def __init__(self, supabase_client: Client):
        """
        Инициализация репозитория с клиентом Supabase.

        Параметры:
        - supabase_client: Client - Клиент для взаимодействия с Supabase.
        """
        self.client = supabase_client

    async def get_nearest(self, employee_id: int):
        """
        Получение информации о графике работы для указанного сотрудника по его ID.

        Параметры:
        - employee_id: int - уникальный идентификатор сотрудника.

        Возвращает:
        - List[dict]: Список ближайших дат для сотрудника.
        - Если данных нет, возвращает пустой список.
        """
        try:
            # Запрос к базе данных для получения ближайших дат сотрудника
            response = self.client.table('Employees')\
            .select('nearest_dates')\
            .eq('user_id', employee_id).execute()
            return response.data if response.data else []
        except Exception as e:
            raise DatabaseResponseException(e)
        
    async def get_employee_attendance(self, employee_id: int, date_start: datetime, date_end: datetime):
        """
        Получение информации о посещаемости сотрудника по его ID.

        Параметры:
        - employee_id: int - уникальный идентификатор сотрудника.
        - date_start: datetime - Начало периода.
        - date_end: datetime - Конец периода.

        Возвращает:
        - List[dict]: Список данных о посещаемости сотрудника.
        """
        try:
            response = self.client.table('EmployeeAttendance')\
            .select('*')\
            .eq('user_id', employee_id)\
            .gte('date', date_start)\
            .lte('date', date_end).execute()
            return response.data if response.data else []
        except Exception as e:
            raise DatabaseResponseException(e)
        
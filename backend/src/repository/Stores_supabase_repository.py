from supabase import Client
from datetime import datetime, timedelta
from collections import defaultdict

from src.repository.interfaces.IStores_repository import IStoreRepository

from src.exception.DatabaseResponseException import DatabaseResponseException


class StoresSupabaseRepository(IStoreRepository):
    """
    Реализация репозитория для работы с магазинами в базе данных Supabase.
    """
    
    def __init__(self, supabase_client: Client):
        """
        Инициализирует репозиторий с клиентом Supabase.

        Параметры:
        - supabase_client: Client - Клиент для взаимодействия с Supabase.
        """
        self.client = supabase_client

    async def get_employees(self, store_id: int):
        """
        Получает список сотрудников для указанного магазина по его ID.
        
        Параметры:
        - store_id: int - Идентификатор магазина.
        
        Возвращает:
        - List[Employee]: Список сотрудников магазина, представленных объектами Employee.
        
        Исключения:
        - DatabaseResponseException: Если возникла ошибка при запросе данных из базы.
        """
        try:
            # Запрос к базе данных для получения сотрудников магазина по его ID
            response = self.client.table('Employees')\
            .select('*')\
            .eq('store_id', store_id).execute()
            return response.data if response.data else []
        except Exception as e:
            raise DatabaseResponseException(e)
        
    async def get_product_available(self, store_id: int, prod_id: str):
        """
        Получает информацию из available конкретного товара в указанном магазине.
        
        Параметры:
        - store_id: int - Идентификатор магазина.
        - prod_id: str - Идентификатор товара.
        
        Возвращает:
        - List[ProductAvailable]: Список available товара по магазинам.
        
        Исключения:
        - DatabaseResponseException: Если возникла ошибка при запросе данных из базы.
        """
        try:
            response = self.client.from_('ProductsAvailable')\
                .select('*')\
                .eq('prod_store_id', store_id)\
                .eq('prod_id', prod_id).execute()
            return response.data if response.data else []
        except Exception as e:
            raise DatabaseResponseException(e)
        
    async def get_product_available_range(self, store_id: int, date_start: datetime, date_end: datetime):
        """
        Получает информацию из available товаров в указанном магазине за указанный период времени.
        
        Параметры:
        - store_id: int - Идентификатор магазина.
        - date_start: datetime - Начало периода.
        - date_end: datetime - Конец периода.
        
        Возвращает:
        - List[ProductAvailable]: Список информацию из available товаров в магазине за указанный период.
        
        Исключения:
        - DatabaseResponseException: Если возникла ошибка при запросе данных из базы.
        """
        try:
            response = self.client.from_('ProductsAvailable')\
                .select('*')\
                .eq('prod_store_id', store_id)\
                .gte('prod_check_time', date_start)\
                .lte('prod_check_time', date_end).execute()
            return response.data if response.data else []
        except Exception as e:
            raise DatabaseResponseException(e)

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
        try:
            # Получаем список всех магазинов
            stores_response = self.client.from_('Stores')\
                .select('id')\
                .execute()

            if not stores_response.data:
                return {}

            store_ids = [store["id"] for store in stores_response.data]

            # Получаем всех сотрудников
            employees_response = self.client.from_('Employees')\
                .select('user_id, store_id')\
                .in_('store_id', store_ids)\
                .execute()

            if not employees_response.data:
                return {}

            # Создаем словарь для сопоставления сотрудников с магазинами
            store_to_users = defaultdict(list)
            for emp in employees_response.data:
                store_to_users[emp["store_id"]].append(emp["user_id"])

            # Получаем все user_id
            all_user_ids = [emp["user_id"] for emp in employees_response.data]

            # Получаем расписания всех сотрудников за период
            attendance_response = self.client.from_('EmployeeAttendance')\
                .select('user_id, date, time, was_present')\
                .in_('user_id', all_user_ids)\
                .gte('date', date_start.strftime("%Y-%m-%d"))\
                .lte('date', date_end.strftime("%Y-%m-%d"))\
                .order('date', desc=False)\
                .order('time', desc=False)\
                .execute()

            # Создаем список всех дат в диапазоне
            date_list = [(date_start + timedelta(days=i)).strftime("%Y-%m-%d")
                        for i in range((date_end - date_start).days + 1)]

            # Словарь для хранения результатов по датам и магазинам
            result_by_date = {date: {} for date in date_list}

            # Собираем все отметки за день для каждого сотрудника
            records_by_user_date = defaultdict(list)
            if attendance_response.data:
                for record in attendance_response.data:
                    key = (record["user_id"], record["date"])
                    records_by_user_date[key].append(record["was_present"])

            # Подсчет присутствующих и отсутствующих по датам и магазинам
            for date in date_list:
                for store_id, user_ids in store_to_users.items():
                    present = 0
                    absent = 0
                    for user_id in user_ids:
                        key = (user_id, date)
                        marks = records_by_user_date.get(key, [])
                        if any(marks):  # хотя бы одна TRUE
                            present += 1
                        else:
                            absent += 1
                    if present > 0 or absent > 0:
                        result_by_date[date][store_id] = {
                            "present": present,
                            "absent": absent
                        }

            return result_by_date

        except Exception as e:
            raise DatabaseResponseException(e)

    async def get_attendance_stat_for_store(self, store_id: int, date_start: datetime, date_end: datetime):
        """
        Получение статистики посещаемости сотрудников по магазину за указанный период.

        Параметры:
        - store_id: int — идентификатор магазина.
        - date_start: datetime — начало временного диапазона.
        - date_end: datetime — конец временного диапазона.

        Возвращает:
        - List[dict]: список словарей с ключами date, employees (user_id, was_present).
        """
        try:
            employees_response = self.client.from_('Employees')\
                .select('user_id')\
                .eq('store_id', store_id)\
                .execute()
            if not employees_response.data:
                return []

            user_ids = [emp["user_id"] for emp in employees_response.data]

            attendance_response = self.client.from_('EmployeeAttendance')\
                .select('user_id, date, was_present')\
                .in_('user_id', user_ids)\
                .gte('date', date_start.strftime("%Y-%m-%d"))\
                .lte('date', date_end.strftime("%Y-%m-%d"))\
                .order('date', desc=False)\
                .order('user_id', desc=False)\
                .execute()

            # Собираем по (user_id, date) — если есть хотя бы одна was_present=True, считаем был
            stat = {}
            if attendance_response.data:
                for record in attendance_response.data:
                    key = (record["user_id"], record["date"])
                    if key not in stat:
                        stat[key] = record["was_present"]
                    else:
                        stat[key] = stat[key] or record["was_present"]

            # Собираем все даты в диапазоне
            date_list = [(date_start + timedelta(days=i)).strftime("%Y-%m-%d")
                         for i in range((date_end - date_start).days + 1)]

            # Группируем по дате
            result = []
            for date in date_list:
                employees = []
                for user_id in user_ids:
                    was_present = stat.get((user_id, date), False)
                    employees.append({
                        "user_id": user_id,
                        "was_present": was_present
                    })
                result.append({
                    "date": date,
                    "employees": employees
                })
            return result

        except Exception as e:
            raise DatabaseResponseException(e)

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
        try:
            response = self.client.from_('Stores')\
                .update({
                    "daily_checks_count": daily_checks_count,
                    "daily_checks_interval": daily_checks_interval
                })\
                .eq('id', store_id)\
                .execute()
            return response.data[0] if response.data else None
        except Exception as e:
            raise DatabaseResponseException(e)

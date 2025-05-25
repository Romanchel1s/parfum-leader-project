from supabase import Client

from src.exception.DatabaseResponseException import DatabaseResponseException

from src.repository.interfaces.IProduct_repository import IProductRepository


class ProductSupabaseRepository(IProductRepository):
    """
    Реализация репозитория для работы с продуктами в базе данных Supabase.
    """
    def __init__(self, supabase_client: Client):
        """
        Инициализация репозитория с клиентом Supabase.

        Параметры:
        - supabase_client: Client - Клиент для взаимодействия с Supabase.
        """
        self.client = supabase_client

        
    async def get_all_product(self):
        """
        Получение списка всех продуктов.

        Возвращает:
        - List[dict]: Список всех продуктов. Если продуктов нет, возвращает пустой список.
        """
        try:
            response = self.client.from_('Products')\
            .select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            raise DatabaseResponseException(e)
        
    async def get_product(self, prod_id: str):
        """
        Получение информации о продукте по его ID.

        Параметры:
        - prod_id: str - уникальный идентификатор продукта.

        Возвращает:
        - dict: Информация о продукте. Если продукт не найден, возвращает пустой словарь.
        """
        try:
            response = self.client.from_('Products').select('*').eq('id', prod_id).execute()
            return response.data if response.data else {}
        except Exception as e:
            raise DatabaseResponseException(e)
        
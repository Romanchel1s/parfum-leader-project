from abc import ABC, abstractmethod


class IProductRepository(ABC):
    """
    Получение информации о всех товарах.

    Параметры:
    - Нет параметров.

    Возвращает:
    - Список объектов с данными о товарах.
    """
    def __init__(self, session, *args):
        """
        Инициализирует репозиторий.

        Параметры:
        - session: объект сессии для работы с базой данных.
        - args: дополнительные аргументы, если требуется.
        """
        raise NotImplementedError()


    @abstractmethod        
    async def get_all_product(self):
        """
        Получение информации о всех товарах.

        Параметры:
        - Нет параметров.

        Возвращает:
        - Список объектов с данными о товарах.
        """
        raise NotImplementedError()
        
    @abstractmethod
    async def get_product(self, prod_id):
        """
        Получение информации о конкретном товаре по его ID.

        Параметры:
        - prod_id: str или int - идентификатор товара.

        Возвращает:
        - Объект с данными о товаре.
        """
        raise NotImplementedError()
        
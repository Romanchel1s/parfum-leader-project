from dependency_injector import containers, providers
from pydantic_settings import BaseSettings
from supabase import create_client, Client

from src.service.IService import IService
from src.service.get_employees_service import GetEmployeesService
from src.service.get_nearest_service import GetNearestService
from src.service.get_all_prod_service import GetAllProductService
from src.service.get_product_service import GetProductService
from src.service.get_product_avaible_service import GetProductAvailable
from src.service.get_product_available_range_service import GetProductAvailableRange
from src.service.get_employee_attendance_service import GetAttendanceService
from src.service.get_nearest_from_store_service import GetNearestFromStoreService
from src.service.get_attendance_stat_for_store_service import GetAttendanceStatForStoreService
from src.service.update_store_check_settings_service import UpdateStoreCheckSettingsService

from src.repository.interfaces.IStores_repository import IStoreRepository
from src.repository.Stores_supabase_repository import StoresSupabaseRepository

from src.repository.interfaces.IEmployees_repository import IEmployeesRepository
from src.repository.Employee_supabase_repository import EmployeesSupabaseRepository

from src.repository.interfaces.IProduct_repository import IProductRepository
from src.repository.Product_supabase_repository import ProductSupabaseRepository


def init_container(settings: BaseSettings):
    """
    Инициализирует контейнер зависимостей для приложения.
    
    Контейнер управляет жизненным циклом сервисов и репозиториев, а также предоставляет их в другие части приложения.
    
    Параметры:
    - settings (BaseSettings): Объект настроек, содержащий параметры для подключения к Supabase.
    
    Возвращает:
    - Container: Контейнер с доступом к репозиториям и сервисам.
    """
    
    class Container(containers.DeclarativeContainer):
        """
        Контейнер зависимостей, управляющий жизненным циклом объектов.
        """
        # Создание экземпляра клиента Supabase
        supabase_client: Client = providers.Singleton(create_client, settings.supabase_settings.url, settings.supabase_settings.key)

        # Репозиторий для работы с данными магазинов
        stores_repository: IStoreRepository = providers.Factory(StoresSupabaseRepository, supabase_client=supabase_client)

        # Сервис для получения списка сотрудников магазинов
        get_employees_service: IService = providers.Factory(GetEmployeesService, repository=stores_repository)
        # Сервис для получения информации о доступности товара в магазине
        get_product_available_service: IService = providers.Factory(GetProductAvailable, repository=stores_repository)
        # Сервис для получения информации о доступности товаров в магазине в заданный период
        get_product_available_range_service: IService = providers.Factory(GetProductAvailableRange, repository=stores_repository)
        # Сервис для получения количества присутствующих и отсутствующих сотрудников во всех магазинах за указанный период
        get_nearest_from_store_service: IService = providers.Factory(GetNearestFromStoreService, repository=stores_repository)
        # Сервис для получения посещаемости сотрудников за указанный период в указанном магазине
        get_attendance_stat_for_store_service: IService = providers.Factory(GetAttendanceStatForStoreService, repository=stores_repository)
        #
        update_store_check_settings_service: IService = providers.Factory(UpdateStoreCheckSettingsService, repository=stores_repository)


        # Репозиторий для работы с данными сотрудников
        employees_repository: IEmployeesRepository = providers.Factory(EmployeesSupabaseRepository, supabase_client=supabase_client)

        # Сервис для получения графика работы сотрудников
        get_nearest_service: IService = providers.Factory(GetNearestService, repository=employees_repository)
        # Сервис для получения информации о посещаемости сотрудников
        get_employee_attendance_service: IService = providers.Factory(GetAttendanceService, repository=employees_repository)


        # Репозиторий для работы с данными о товарах
        product_repository: IProductRepository = providers.Factory(ProductSupabaseRepository, supabase_client=supabase_client)

        # Сервис для получения всех продуктов
        get_all_product_service: IService = providers.Factory(GetAllProductService, repository=product_repository)
         # Сервис для получения информации о конкретном товаре
        get_product_service: IService = providers.Factory(GetProductService, repository=product_repository)

    container = Container()

    return container

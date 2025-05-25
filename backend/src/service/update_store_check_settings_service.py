from pydantic import ValidationError

from src.schema.store_check_settings_update import StoreCheckSettingsUpdate

from src.repository.interfaces.IStores_repository import IStoreRepository

from src.service.IService import IService

from src.exception.CustomException import CustomException
from src.exception.ResourseNotFoundException import ResourceNotFoundException
from src.exception.ServerValidationException import ServerValidationException


class UpdateStoreCheckSettingsService(IService[dict]):
    """
    Сервис для обновления настроек периодичности проверки товара для магазина.

    Параметры:
    - repository: IStoreRepository — репозиторий магазинов.

    Возвращает:
    - dict: обновлённые данные магазина.
    """
    def __init__(self, repository: IStoreRepository):
        self.repository = repository

    async def execute(self, store_id: int, settings: StoreCheckSettingsUpdate) -> dict:
        """
        Обновление настроек периодичности проверки товара для магазина.

        Параметры:
        - store_id: int — идентификатор магазина.
        - settings: StoreCheckSettingsUpdate — новые настройки.

        Возвращает:
        - dict: обновлённые данные магазина.
        """
        try:
            data = await self.repository.update_store_check_settings(
                store_id,
                settings.daily_checks_count,
                settings.daily_checks_interval
            )
            if not data:
                raise ResourceNotFoundException('Магазин не найден или не удалось обновить настройки')
            return data
        
        except ValidationError as e:
            raise ServerValidationException(e)
        
        except Exception as e:
            raise CustomException(e) 

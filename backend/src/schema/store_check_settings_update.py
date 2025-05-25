from pydantic import BaseModel, Field


class StoreCheckSettingsUpdate(BaseModel):
    """
    Модель для обновления настроек периодичности проверки товара в магазине.

    Параметры:
    - daily_checks_count: int — количество проверок в день.
    - daily_checks_interval: int — интервал между проверками (например, в часах).
    """
    daily_checks_count: int = Field(..., description="Количество проверок в день")
    daily_checks_interval: int = Field(..., description="Интервал между проверками")
    
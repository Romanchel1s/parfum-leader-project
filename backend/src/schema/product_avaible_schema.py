from pydantic import BaseModel, Field
from datetime import datetime


class ProductAvailable(BaseModel):
    """
    Модель данных для информации о наличии товара.

    Атрибуты:
        - `prod_id`: Идентификатор товара.
        - `prod_avail`: Флаг, указывающий на наличие товара (True, если товар доступен).
        - `prod_check_time`: Время проверки наличия товара.
        - `prod_store_id`: Идентификатор магазина, где проверяется товар.
        - `prod_employee_id`: Идентификатор сотрудника, который проверил наличие товара.
    """
    prod_id: str = Field(..., description="ID товара")
    prod_avail: bool = Field(..., description="наличие товара")
    prod_check_time: datetime = Field(..., description="дата")
    prod_store_id: int = Field(..., description="код магазина")
    prod_employee_id: int = Field(..., description="ID сотрудника")

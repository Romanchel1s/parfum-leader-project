from pydantic import BaseModel, Field
from typing import Dict


class Employee(BaseModel):
    """
    Модель данных для сотрудника магазина.

    Атрибуты:
        - `username`: Имя сотрудника.
        - `store_id`: Идентификатор магазина, в котором работает сотрудник.
        - `phone_number`: Номер телефона сотрудника.
        - `user_id`: Уникальный идентификатор сотрудника.
        - `nearest_dates`: Расписание сотрудника, представленное в виде словаря, где ключ — дата, а значение — описание рабочего дня.
    """
    username: str = Field(..., description="имя сотрудника")
    store_id: int = Field(..., description="ID магазина")
    phone_number: str = Field(..., description="Номер телефона")
    user_id: int = Field(..., description="ID сотрудника")
    nearest_dates: Dict[str, str] = Field(..., description="Расписание сотрудника")

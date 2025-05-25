from pydantic import BaseModel, Field
from typing import List


class NearestFromStore(BaseModel):
    """
    Модель для информации о посещаемости по одному магазину за день.

    Параметры:
    - store_id: int — ID магазина.
    - present: int — количество присутствующих.
    - absent: int — количество отсутствующих.
    """
    store_id: int = Field(..., description="ID магазина")
    present: int = Field(..., description="количество присутствующих")
    absent: int = Field(..., description="количество отсутствующих")


class NearestFromStoreByDate(BaseModel):
    """
    Модель для информации о посещаемости по всем магазинам за конкретную дату.

    Параметры:
    - date: str — дата.
    - stores: List[NearestFromStore] — список информации по каждому магазину.
    """
    date: str = Field(..., description="Дата")
    stores: List[NearestFromStore] = Field(..., description="Информация по магазинам")
    
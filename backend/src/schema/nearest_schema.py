from pydantic import BaseModel, Field
from typing import Dict


class Nearest(BaseModel):
    """
    Модель данных для расписания сотрудника.

    Атрибуты:
        - `nearest_dates`: Расписание сотрудника в виде словаря, где ключ — дата, а значение — описание рабочего дня.
    """
    nearest_dates: Dict[str, str] = Field(..., description="Расписание сотрудника", default_factory=dict)

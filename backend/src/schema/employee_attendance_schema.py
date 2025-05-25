from pydantic import BaseModel, Field
import datetime


class EmployeeAttendance(BaseModel):
    """
    Модель для представления посещаемости сотрудника.
    
    Атрибуты:
        - `id`: Уникальный идентификатор записи посещаемости.
        - `user_id`: Идентификатор сотрудника.
        - `date`: Дата посещения.
        - `time`: Время посещения.
        - `was_present`: Статус присутствия (True или False).
    """
    id: int = Field(..., description="ID записи")
    user_id: int = Field(..., description="ID сотрудника")
    date: datetime.date = Field(..., description="Дата")
    time: datetime.time = Field(..., description="Время")
    was_present: bool = Field(..., description="was present")

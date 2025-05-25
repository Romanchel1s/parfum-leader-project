from pydantic import BaseModel, Field
from typing import List


class EmployeeAttendanceShort(BaseModel):
    """
    Краткая информация о посещаемости сотрудника за день.

    Параметры:
    - user_id: int — ID сотрудника.
    - was_present: bool — был ли сотрудник в этот день.
    """
    user_id: int = Field(..., description="ID сотрудника")
    was_present: bool = Field(..., description="Был ли сотрудник в этот день")


class EmployeeAttendanceStatByDate(BaseModel):
    """
    Информация о посещаемости сотрудников по дате.

    Параметры:
    - date: str — дата.
    - employees: List[EmployeeAttendanceShort] — список сотрудников и их присутствие.
    """
    date: str = Field(..., description="Дата")
    employees: List[EmployeeAttendanceShort] = Field(..., description="Список сотрудников и их присутствие") 

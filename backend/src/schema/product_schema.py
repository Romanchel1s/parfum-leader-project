from pydantic import BaseModel, Field


class Product(BaseModel):
    """
    Модель данных для продукта.

    Атрибуты:
        - `id`: Идентификатор товара.
        - `name`: Название товара.
        - `beautiful_name`: beautiful_name.
        - `stock`: Количество товара в наличии.
        - `photo_url`: URL изображения товара.
        - `url`: url.
    """
    id: str = Field(..., description="ID товара")
    name: str = Field(..., description="Название товара")
    beautifulName: str = Field(..., description="beautiful_name")
    stock: str = Field(..., description="Количество товара в наличии")
    photo: str = Field(..., description="URL изображения товара")
    URL: str = Field(..., description="url")

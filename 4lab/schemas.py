from pydantic import BaseModel, Field
from typing import List, Optional

from pydantic import BaseModel, Field
from typing import List, Optional


class StoreBase(BaseModel):
    name: str = Field(..., max_length=100)
    address: str = Field(..., max_length=200)


class StoreCreate(StoreBase):
    pass


class Store(StoreBase):
    id: int

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str = Field(..., max_length=100)
    price: float = Field(..., gt=0)
    store_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  # Заменили orm_mode на from_attributes
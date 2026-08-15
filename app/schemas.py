from pydantic import BaseModel
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    sku: str
    quantity: int
    price: float

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
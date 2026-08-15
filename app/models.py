from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    sku = Column(String, unique=True, index=True)
    quantity = Column(Integer, default=0)
    price = Column(Numeric(10, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
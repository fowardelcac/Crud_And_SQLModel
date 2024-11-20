from typing import Optional
from decimal import Decimal
from sqlmodel import Field, SQLModel


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class Purchase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: Decimal = Field(default=0, max_digits=5, decimal_places=2)
    unit_price: Decimal = Field(default=0, max_digits=10, decimal_places=2)
    total: Decimal = Field(default=0, max_digits=20, decimal_places=2)

    product_id: Optional[int] = Field(default=None, foreign_key="product.id")

class Receipt(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str
    purchase_id: Optional[int] = Field(default=None, foreign_key="purchase.id")

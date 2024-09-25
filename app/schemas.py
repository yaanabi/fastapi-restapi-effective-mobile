from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Annotated

from .enums import OrderStatus


class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: Annotated[float, Field(ge=0.0)]
    quantity_in_stock: Annotated[int, Field(ge=0)]

class ProductRead(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductCreate(ProductBase):
    pass


class OrderItemBase(BaseModel):
    product_id: int
    quantity: Annotated[int, Field(gt=0)]


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    order_id: int

class OrderBase(BaseModel):
    pass


class OrderRead(OrderBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    order_items: list[OrderItemCreate]
    status: OrderStatus = OrderStatus.IN_PROCESS


class OrderCreate(OrderBase):
    order_items: Annotated[list[OrderItemCreate], Field(min_length=1)]


class OrderUpdateStatus(OrderBase):
    status: OrderStatus = OrderStatus.IN_PROCESS

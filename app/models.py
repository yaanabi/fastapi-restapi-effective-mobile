from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, String, Enum
from sqlalchemy.sql import func
from .enums import OrderStatus


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]]
    price: Mapped[float]
    quantity_in_stock: Mapped[int]
    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self):
        return f"Product(id={self.id!r}, name={self.name!r}, description={self.description!r}, price={self.price!r}, quantity_in_stock={self.quantity_in_stock!r}, is_deleted={self.is_deleted!r}, order_items={self.order_items!r})"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime,
                                                 server_default=func.now())
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus),
                                                default=OrderStatus.IN_PROCESS,
                                                nullable=False)

    def __repr__(self):
        return f"Order(id={self.id!r}, created_at={self.created_at!r}, status={self.status!r}, order_items={self.order_items!r})"


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"))
    quantity: Mapped[int]
    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items')

    def __repr__(self):
        return f"OrderItem(id={self.id!r}, order_id={self.order_id!r}, product_id={self.product_id!r}, quantity={self.quantity!r})"


Order.order_items = relationship('OrderItem',
                                 order_by=OrderItem.id,
                                 back_populates='order')
Product.order_items = relationship('OrderItem',
                                   back_populates='product',
                                   cascade="all, delete-orphan")

from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session

from ..services import order_service
from ..models import OrderStatus
import app.schemas as schemas
from ..db import get_db

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/", response_model=list[schemas.OrderRead])
def read_orders(db: Annotated[Session, Depends(get_db)]):
    return order_service.get_all_orders(db)


@router.post("/",
             response_model=schemas.OrderRead,
             status_code=status.HTTP_201_CREATED)
def create_order(order_items: Annotated[schemas.OrderCreate, Depends()], db: Annotated[Session,
                                                         Depends(get_db)]):
    return order_service.create_order(order_items.model_dump(), db)


@router.get("/{order_id}", response_model=schemas.OrderRead)
def read_order(order_id: int, db: Annotated[Session, Depends(get_db)]):
    order = order_service.get_order_by_id(order_id, db)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/status", response_model=schemas.OrderRead)
def update_order(order_id: int, order: Annotated[schemas.OrderUpdateStatus,
                                                 Form()],
                 db: Annotated[Session, Depends(get_db)]):
    return order_service.update_order_status(order_id, order, db)


# @router.delete("/{order_id}", response_model=schemas.OrderRead)
# def delete_order(order_id: int, db: Annotated[Session, Depends(get_db)]):
#     return order_service.delete_order(order_id, db)

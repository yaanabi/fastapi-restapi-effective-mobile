from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import Order
import app.schemas as schemas



def read_orders(db: Session):
    return db.query(Order).all()


def read_order(order_id: int, db: Session):
    db_order =  db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order


def create_order(order: Order, db: Session):
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def update_order_status(order_id: int, order: schemas.OrderCreate, db: Session):
    db_order = read_order(order_id, db)
    if db_order:
        db_order.status = order.status
        db.commit()
        db.refresh(db_order)
    return db_order


# def delete_order(order_id: int, db: Session):
#     db_order = read_order(order_id, db)
#     if db_order:
#         db.delete(db_order)
#         db.commit()
#     return db_order

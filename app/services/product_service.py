from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models import Product, Order
from ..repos import product_crud


def get_products(db: Session):
    return product_crud.read_products(db)


def get_product_by_id(product_id: int, db: Session):
    db_product = product_crud.read_product(product_id, db)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


def create_product(product: Product, db: Session):
    db_product = product_crud.create_product(product, db)
    return db_product


def update_product(product_id: int, product: Product, db: Session):
    db_product = product_crud.update_product(product_id, product, db)
    return db_product


def delete_product(product_id: int, db: Session):
    db_product = product_crud.read_product(product_id, db)
    order_items = db_product.order_items
    order_ids = [item.order_id for item in order_items]
    # Fetch all orders at once with a single query
    db_orders = db.query(Order).filter(Order.id.in_(order_ids)).all()
    # Create a dictionary of order.id -> Order for quick access
    order_map = {order.id: order for order in db_orders}
    for order_item in order_items:
        order = order_map.get(order_item.order_id)
        if order and order.status.name == 'IN_PROCESS':
            raise HTTPException(
                status_code=400,
                detail="Cannot delete product that is currently being processed"
            )

    return product_crud.delete_product(product_id, db)

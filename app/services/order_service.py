from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import Order, Product, OrderItem
from ..repos import order_crud
import app.schemas as schemas


def get_all_orders(db: Session):
    return order_crud.read_orders(db)


def get_order_by_id(order_id: int, db: Session):
    return order_crud.read_order(order_id, db)


def create_order(order_items: schemas.OrderCreate, db: Session):
    order = Order()
    product_ids = [item['product_id'] for item in order_items['order_items']]

    # Fetch all products at once with a single query
    db_products = db.query(Product).filter(Product.id.in_(product_ids)).all()
    # Create a dictionary of product_id -> Product for quick access
    product_map = {product.id: product for product in db_products}

    products = order_items['order_items']
    model_order_items = []
    for product in products:

        db_product = product_map.get(product['product_id'])
        if not db_product:
            raise HTTPException(
                status_code=404,
                detail=f"Product(id={product['product_id']}) not found")
        if db_product.quantity_in_stock < product['quantity']:
            raise HTTPException(
                status_code=400,
                detail=
                f"Insufficient stock for product_id: {product['product_id']} (stock: {db_product.quantity_in_stock})"
            )
        if product['quantity'] == 0:
            raise HTTPException(status_code=400,
                                detail="Quantity cannot be zero")
        db_product.quantity_in_stock -= product['quantity']
        model_order_items.append(
            OrderItem(order_id=order.id,
                      product_id=product['product_id'],
                      quantity=product['quantity']))

    order.order_items = model_order_items
    return order_crud.create_order(order, db)


def update_order_status(order_id: int, order: Order, db: Session):
    return order_crud.update_order_status(order_id, order, db)


# def delete_order(order_id: int, db: Session):
#     return order_crud.delete_order(order_id, db)

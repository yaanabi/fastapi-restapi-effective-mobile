from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import Product
import app.schemas as schemas


def read_products(db: Session):
    return db.query(Product).filter(Product.is_deleted == False).all()


def read_product(product_id: int, db: Session):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product or db_product.is_deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    if db_product.is_deleted == False:
        return db_product


def create_product(product: schemas.ProductCreate, db: Session):
    product_create = Product(**product.model_dump())
    db.add(product_create)
    db.commit()
    db.refresh(product_create)
    return product_create


def update_product(product_id: int, product: schemas.ProductCreate,
                   db: Session):
    db_product = read_product(product_id, db)
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity_in_stock = product.quantity_in_stock
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(product_id: int, db: Session):
    db_product = read_product(product_id, db)
    if db_product:
        db_product.is_deleted = True
        db.commit()
    return db_product

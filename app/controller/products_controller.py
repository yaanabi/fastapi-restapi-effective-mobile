from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.orm import Session

from ..services import product_service
import app.schemas as schemas

from ..db import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[schemas.ProductRead])
def read_products(db: Annotated[Session, Depends(get_db)]):
    return product_service.get_products(db)


@router.get("/{product_id}", response_model=schemas.ProductRead)
def read_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    return product_service.get_product_by_id(product_id, db)


@router.post("/",
             response_model=schemas.ProductRead,
             status_code=status.HTTP_201_CREATED)
def create_product(product: Annotated[schemas.ProductCreate,
                                      Form()], db: Annotated[Session,
                                                             Depends(get_db)]):
    return product_service.create_product(product, db)


@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: int, product: Annotated[schemas.ProductCreate,
                                                       Form()],
                   db: Annotated[Session, Depends(get_db)]):
    return product_service.update_product(product_id, product, db)


@router.delete("/{product_id}", response_model=schemas.ProductRead)
def delete_product(product_id: int, db: Annotated[Session, Depends(get_db)]):
    return product_service.delete_product(product_id, db)

from fastapi import FastAPI
from .controller.products_controller import router as products_router
from .controller.orders_controller import router as orders_router
from .models import Base
from .db import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(products_router)
app.include_router(orders_router)

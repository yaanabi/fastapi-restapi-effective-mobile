import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models import Base, Product
from app.db import get_db
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
DB_TEST_URL = os.getenv("DB_TEST_URL")
engine = create_engine(DB_TEST_URL)

TestingSessionLocal = sessionmaker(bind=engine,
                                   autocommit=False,
                                   autoflush=False)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db_session():
    """Create a new database session with a rollback at the end of the test."""

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="module")
def test_product_id(db_session):
    product = Product(name="Test Product",
                      description="This is a test product",
                      price=10.99,
                      quantity_in_stock=5)
    db_session.add(product)
    db_session.commit()
    yield product.id


@pytest.fixture(scope="module")
def test_client(db_session):
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
